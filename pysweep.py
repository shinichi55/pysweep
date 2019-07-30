#!/usr/bin/python3

# Write your output to a a file named: pingsweep-results.txt.
file = open( 'pingsweep-results.txt', 'w' )

import sys
# Import and use the Python subprocess mobudle at the top of your script.
import subprocess

# Define a variable named ip_target that contains the first 3 octets of a Class C IP address, /24 CIDR.
ip_target = [ sys.argv[1] ]
output_list = []

# Write a main function that will be the initial function called by your application.
def main():
        # Using a standard for loop and the subprocess.call() method, write a function that loops over all 256 possible IP addresses and does the following:
        for ip in ip_target:
                # Calls the fping command line utility to send an ICMP ping to the address with the following flags:
                # -a - Show systems that are alive.
                # -C 5 - Show latency times of 5 requests to the host.
                # -q - Show only final sumamry and not line by line results.
                if '/' in ip:
                        # Store the response in a variable.
                        output = subprocess.Popen( ['fping', '-a', '-C 5', '-q', '-g', ip], stderr = subprocess.PIPE, universal_newlines = True )
                        for item in output.stderr:
                                output_list.append( item.replace( '\n', '' ) )
                        return
                else:
                        output = subprocess.Popen( ['fping', '-a', '-C 5', '-q', ip], stderr = subprocess.PIPE, universal_newlines = True )
                        for item in output.stderr:
                                output_list.append( item.replace( '\n', '' ) )
                        return
        return

out_ip = []
out_resp = []

def split_main():        
        # Split the response into variables that hold the IP address and the response in separate varaibles.
        # Store the IP addresses in a list.
        for out in output_list:
                if ': - - - - -' in out:
                        continue
                elif 'duplicate' in out:
                        continue
                else:
                        out_split = out.split( ' : ' )
                        x = out_split[0]
                        y = out_split[1]
                        out_ip.append( x )
                        out_resp.append( y )
                        # Print out the following output for each IP address.
                        # Print out only hosts that are on the network in the following format:
                        file.write( 'Host: {} is detected online. Response time(s) were: {}'.format(x, y) + '\n' )
        return

resp_list = []

def resp_main():
        # Total time to scan took: xxxms
        for resp in out_resp:
                resp_output = resp.translate( {ord( '-' ): '0' } ).split( ' ' )
                resp_float = [float(i) for i in resp_output]
                resp_list.append( sum(resp_float) )
        return

# Upon completion of all hosts, print a sumamry with the following format:
def print_main():
        file.write( '\n' + 'The following hosts were found to be online and responding to ping requests:' + '\n' )
        file.write( '\n' + 'Detected Hosts:' + '\n' ) 
        file.write( '===============' + '\n' )
        for host in out_ip:
                file.write( host + '\n' )
        file.write( '\n' + 'Total time to scan took: ' + str(sum(resp_list)) + 'ms' )
        return

if __name__ == "__main__":
    main()
    split_main()
    resp_main()
    print_main()

file.close()

# Use the git add . command to add your changes to git.
# Add a commit message using the git commit -m "" command.
# Push your code to Github using the git push -u origin master command.
# Update your for loop to scan only the number of hosts that are part of that subnet mask and maintain the same functionality.
# Add readme.md with documentation fo how to use the tool.