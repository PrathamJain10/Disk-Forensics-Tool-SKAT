#!/usr/bin/env python3
"""
Sleuth Kit Automation Tool (SKAT)

A command-line utility that automates common digital forensics tasks using The Sleuth Kit (TSK).
This tool simplifies the process of acquiring and analyzing digital evidence.
"""

import os
import sys
import argparse
import subprocess
import json
import logging
import datetime
import hashlib
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("skat.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SKAT")

class SleuthKitAutomationTool:
    def __init__(self):
        self.evidence_dir = "evidence"
        self.reports_dir = "reports"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure directories exist
        for directory in [self.evidence_dir, self.reports_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def verify_tsk_installation(self):
        """Verify that necessary Sleuth Kit tools are installed."""
        required_tools = ["mmls", "fls", "icat", "blkcat", "fsstat", "mmstat"]
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run([tool, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError:
                missing_tools.append(tool)
        
        if missing_tools:
            logger.error(f"Missing required Sleuth Kit tools: {', '.join(missing_tools)}")
            logger.error("Please install The Sleuth Kit: https://www.sleuthkit.org/sleuthkit/download.php")
            return False
        
        logger.info("Sleuth Kit installation verified")
        return True
    
    def acquire_image(self, source, output=None):
        """Create a forensic image of the source disk or partition."""
        if not output:
            output = os.path.join(self.evidence_dir, f"image_{self.timestamp}.dd")
        
        logger.info(f"Creating forensic image of {source} to {output}")
        
        try:
            # Using dd for acquisition
            cmd = ["dd", f"if={source}", f"of={output}", "bs=4M", "conv=sync,noerror", "status=progress"]
            subprocess.run(cmd, check=True)
            
            # Calculate hash for verification
            md5_hash = self._calculate_hash(output, "md5")
            sha1_hash = self._calculate_hash(output, "sha1")
            
            # Save acquisition metadata
            metadata = {
                "source": source,
                "image_path": output,
                "acquisition_date": datetime.datetime.now().isoformat(),
                "md5": md5_hash,
                "sha1": sha1_hash
            }
            
            with open(f"{output}.json", "w") as f:
                json.dump(metadata, f, indent=4)
            
            logger.info(f"Image acquisition complete: {output}")
            logger.info(f"MD5: {md5_hash}")
            logger.info(f"SHA1: {sha1_hash}")
            
            return output
        except subprocess.SubprocessError as e:
            logger.error(f"Image acquisition failed: {e}")
            return None
    
    def _calculate_hash(self, file_path, algorithm):
        """Calculate hash of a file using the specified algorithm."""
        hash_func = None
        if algorithm == "md5":
            hash_func = hashlib.md5()
        elif algorithm == "sha1":
            hash_func = hashlib.sha1()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        with open(file_path, "rb") as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def analyze_partitions(self, image_path):
        """Analyze partition structure of the image."""
        output_file = os.path.join(self.reports_dir, f"partitions_{Path(image_path).stem}_{self.timestamp}.txt")
        
        logger.info(f"Analyzing partitions in {image_path}")
        
        try:
            # Run mmls to get partition layout
            result = subprocess.run(["mmls", image_path], check=True, 
                                    stdout=subprocess.PIPE, text=True)
            
            with open(output_file, "w") as f:
                f.write(f"Partition Analysis for {image_path}\n")
                f.write("=" * 80 + "\n")
                f.write(result.stdout)
            
            logger.info(f"Partition analysis saved to {output_file}")
            return output_file
        except subprocess.SubprocessError as e:
            logger.error(f"Partition analysis failed: {e}")
            return None
    
    def extract_filesystem_stats(self, image_path, offset=0):
        """Extract filesystem statistics from the image."""
        output_file = os.path.join(self.reports_dir, f"fsstat_{Path(image_path).stem}_{self.timestamp}.txt")
        
        logger.info(f"Extracting filesystem stats from {image_path} at offset {offset}")
        
        try:
            # Run fsstat to get filesystem information
            cmd = ["fsstat"]
            if offset > 0:
                cmd.extend(["-o", str(offset)])
            cmd.append(image_path)
            
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True)
            
            with open(output_file, "w") as f:
                f.write(f"Filesystem Analysis for {image_path} (Offset: {offset})\n")
                f.write("=" * 80 + "\n")
                f.write(result.stdout)
            
            logger.info(f"Filesystem analysis saved to {output_file}")
            return output_file
        except subprocess.SubprocessError as e:
            logger.error(f"Filesystem analysis failed: {e}")
            return None
    
    def list_files(self, image_path, offset=0, recursive=True):
        """List files in the filesystem from the image."""
        output_file = os.path.join(self.reports_dir, f"filelist_{Path(image_path).stem}_{self.timestamp}.txt")
        
        logger.info(f"Listing files from {image_path} at offset {offset}")
        
        try:
            # Run fls to list files
            cmd = ["fls", "-r" if recursive else ""]
            if offset > 0:
                cmd.extend(["-o", str(offset)])
            cmd.append(image_path)
            
            result = subprocess.run([c for c in cmd if c], check=True, 
                                   stdout=subprocess.PIPE, text=True)
            
            with open(output_file, "w") as f:
                f.write(f"File Listing for {image_path} (Offset: {offset})\n")
                f.write("=" * 80 + "\n")
                f.write(result.stdout)
            
            logger.info(f"File listing saved to {output_file}")
            return output_file
        except subprocess.SubprocessError as e:
            logger.error(f"File listing failed: {e}")
            return None
    
    def extract_file(self, image_path, inode, output=None, offset=0):
        """Extract a specific file by inode from the image."""
        if not output:
            output = os.path.join(self.evidence_dir, f"inode_{inode}_{self.timestamp}.bin")
        
        logger.info(f"Extracting inode {inode} from {image_path} to {output}")
        
        try:
            # Run icat to extract the file
            cmd = ["icat"]
            if offset > 0:
                cmd.extend(["-o", str(offset)])
            cmd.extend([image_path, str(inode)])
            
            with open(output, "wb") as f:
                subprocess.run(cmd, check=True, stdout=f)
            
            logger.info(f"File extraction complete: {output}")
            return output
        except subprocess.SubprocessError as e:
            logger.error(f"File extraction failed: {e}")
            return None
    
    def timeline_analysis(self, image_path, offset=0):
        """Create a timeline of file activity."""
        body_file = os.path.join(self.reports_dir, f"body_file_{Path(image_path).stem}_{self.timestamp}")
        timeline_file = os.path.join(self.reports_dir, f"timeline_{Path(image_path).stem}_{self.timestamp}.txt")
        
        logger.info(f"Creating timeline for {image_path}")
        
        try:
            # Create body file
            cmd = ["fls", "-m", "/", "-r"]
            if offset > 0:
                cmd.extend(["-o", str(offset)])
            cmd.append(image_path)
            
            with open(body_file, "w") as f:
                subprocess.run(cmd, check=True, stdout=f)
            
            # Create timeline from body file
            with open(timeline_file, "w") as f:
                subprocess.run(["mactime", "-b", body_file], check=True, stdout=f)
            
            logger.info(f"Timeline analysis saved to {timeline_file}")
            return timeline_file
        except subprocess.SubprocessError as e:
            logger.error(f"Timeline analysis failed: {e}")
            return None
    
    def run_autopsy(self, evidence_path):
        """Launch Autopsy with the specified evidence."""
        logger.info(f"Attempting to launch Autopsy with {evidence_path}")
        
        try:
            # Check if Autopsy is installed
            subprocess.run(["which", "autopsy"], check=True, stdout=subprocess.PIPE)
            
            # Launch Autopsy (actual implementation may vary based on system)
            subprocess.Popen(["autopsy", evidence_path])
            
            logger.info("Autopsy launched successfully")
            return True
        except subprocess.SubprocessError:
            logger.error("Failed to launch Autopsy. Is it installed?")
            return False
    
    def run_full_analysis(self, image_path, offset=0):
        """Run a full analysis workflow on the image."""
        logger.info(f"Starting full analysis on {image_path}")
        
        results = {
            "image": image_path,
            "offset": offset,
            "timestamp": self.timestamp,
            "reports": {}
        }
        
        # Analyze partitions
        results["reports"]["partitions"] = self.analyze_partitions(image_path)
        
        # Extract filesystem information
        results["reports"]["filesystem"] = self.extract_filesystem_stats(image_path, offset)
        
        # List files
        results["reports"]["file_list"] = self.list_files(image_path, offset)
        
        # Create timeline
        results["reports"]["timeline"] = self.timeline_analysis(image_path, offset)
        
        # Save analysis results
        summary_file = os.path.join(self.reports_dir, f"analysis_summary_{Path(image_path).stem}_{self.timestamp}.json")
        with open(summary_file, "w") as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"Full analysis complete. Summary saved to {summary_file}")
        return summary_file

def main():
    parser = argparse.ArgumentParser(description='Sleuth Kit Automation Tool (SKAT)')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify TSK installation')
    
    # Acquire command
    acquire_parser = subparsers.add_parser('acquire', help='Create forensic image')
    acquire_parser.add_argument('source', help='Source disk or partition')
    acquire_parser.add_argument('--output', '-o', help='Output image file')
    
    # Analyze partitions command
    part_parser = subparsers.add_parser('partitions', help='Analyze partition structure')
    part_parser.add_argument('image', help='Path to forensic image')
    
    # Filesystem stats command
    fs_parser = subparsers.add_parser('fsstat', help='Extract filesystem statistics')
    fs_parser.add_argument('image', help='Path to forensic image')
    fs_parser.add_argument('--offset', '-o', type=int, default=0, help='Partition offset')
    
    # List files command
    ls_parser = subparsers.add_parser('list', help='List files in the filesystem')
    ls_parser.add_argument('image', help='Path to forensic image')
    ls_parser.add_argument('--offset', '-o', type=int, default=0, help='Partition offset')
    ls_parser.add_argument('--no-recursive', '-n', action='store_true', help='Non-recursive listing')
    
    # Extract file command
    extract_parser = subparsers.add_parser('extract', help='Extract file by inode')
    extract_parser.add_argument('image', help='Path to forensic image')
    extract_parser.add_argument('inode', type=int, help='Inode to extract')
    extract_parser.add_argument('--offset', '-o', type=int, default=0, help='Partition offset')
    extract_parser.add_argument('--output', help='Output file path')
    
    # Timeline command
    timeline_parser = subparsers.add_parser('timeline', help='Create activity timeline')
    timeline_parser.add_argument('image', help='Path to forensic image')
    timeline_parser.add_argument('--offset', '-o', type=int, default=0, help='Partition offset')
    
    # Autopsy command
    autopsy_parser = subparsers.add_parser('autopsy', help='Launch Autopsy with evidence')
    autopsy_parser.add_argument('evidence', help='Path to evidence file')
    
    # Full analysis command
    full_parser = subparsers.add_parser('full', help='Run full analysis')
    full_parser.add_argument('image', help='Path to forensic image')
    full_parser.add_argument('--offset', '-o', type=int, default=0, help='Partition offset')
    
    args = parser.parse_args()
    
    # Create tool instance
    tool = SleuthKitAutomationTool()
    
    # Process commands
    if args.command == 'verify':
        tool.verify_tsk_installation()
    elif args.command == 'acquire':
        tool.acquire_image(args.source, args.output)
    elif args.command == 'partitions':
        tool.analyze_partitions(args.image)
    elif args.command == 'fsstat':
        tool.extract_filesystem_stats(args.image, args.offset)
    elif args.command == 'list':
        tool.list_files(args.image, args.offset, not args.no_recursive)
    elif args.command == 'extract':
        tool.extract_file(args.image, args.inode, args.output, args.offset)
    elif args.command == 'timeline':
        tool.timeline_analysis(args.image, args.offset)
    elif args.command == 'autopsy':
        tool.run_autopsy(args.evidence)
    elif args.command == 'full':
        tool.run_full_analysis(args.image, args.offset)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()