#!/usr/bin/python3

# Write your output to a a file named: pingsweep-results.txt.
file = open( 'pingsweep-results.txt', 'w' )

import sys
# Import and use the Python subprocess mobudle at the top of your script.
import subprocess

# Define a variable named ip_target that contains the first 3 octets of a Class C IP address, /24 CIDR.
# Update your function to use two variables:
# An IP address.
# A CIDR block size ex. /24 or /27.
# Have your script take in arguments for both IP CIDR values.
# Ex. ./pysweep.py 192.168.0.1 /24.
ip_target = [ sys.argv[1] ]

# Write a main function that will be the initial function called by your application.
def main():
        alive_list = []
        # Using a standard for loop and the subprocess.call() method, write a function that loops over all 256 possible IP addresses and does the following:
        for alive_ip in ip_target:
                # Calls the fping command line utility to send an ICMP ping to the address with the following flags:
                # -a - Show systems that are alive.
                # -q - Show only final sumamry and not line by line results.
                if '/' in alive_ip:
                        # Store the response in a variable.
                        alive = subprocess.Popen( ['fping', '-a', '-q', '-g', alive_ip], stdout = subprocess.PIPE, universal_newlines = True )
                        for item in alive.stdout:
                                alive_list.append( item.replace( '\n', '' ) )
                                continue
                else:
                        alive = subprocess.Popen( ['fping', '-a', '-q', alive_ip], stdout = subprocess.PIPE, universal_newlines = True )
                        for item in alive.stdout:
                                alive_list.append( item.replace( '\n', '' ) )
                                continue

        output_list = []
        for ip in alive_list:
                # -C 5 - Show latency times of 5 requests to the host.
                output = subprocess.Popen( ['fping', '-C 5', '-q', ip], stderr = subprocess.PIPE, universal_newlines = True )
                for line in output.stderr:
                                output_list.append( line.replace( '\n', '' ) )
                                continue
        
                # Split the response into variables that hold the IP address and the response in separate varaibles.
                # Store the IP addresses in a list.
                out_ip = []
                out_resp = []
                for out in output_list:
                        out_split = out.split( ' : ' )
                        out_ip.append( out_split[0] )
                        out_resp.append( out_split[1] )

                        # Print out the following output for each IP address.
                        # Print out only hosts that are on the network in the following format:
                        for ip_out in out_ip:
                                x = ip_out
                        for resp_out in out_resp:
                                y = resp_out
                
                file.write( 'Host: {} is detected online. Response time(s) were: {}'.format(x, y) + '\n' )

                # Total time to scan took: xxxms
                resp_list = []
                for resp in out_resp:
                        resp_str = resp.translate( {ord( '-' ): '0' } ).split( ' ' )
                        resp_flt = [float(i) for i in resp_str]
                        resp_list.append( sum( resp_flt ) )

                print( sum(resp_list) )

        # Upon completion of all hosts, print a sumamry with the following format:
        file.write( '\n' + 'The following hosts were found to be online and responding to ping requests:' + '\n' )
        file.write( '\n' + 'Detected Hosts:' + '\n' ) 
        file.write( '===============' + '\n' )
        for host in out_ip:
                file.write( host + '\n' )
        file.write( '\n' + 'Total time to scan took: ' + str(sum(resp_list)) + 'ms' )
        return

if __name__ == "__main__":
    main()

file.close()

# Use the git add . command to add your changes to git.
# Add a commit message using the git commit -m "" command.
# Push your code to Github using the git push -u origin master command.
# Update your for loop to scan only the number of hosts that are part of that subnet mask and maintain the same functionality.
# Add readme.md with documentation fo how to use the tool.