import re
from pathlib import Path

######################################################################
#                                                                    #
#                             NOTES:                                 #
#     -For the trimmer to work, you must have all of the log         #
#     files in the same directory as this py file, and their         #
#     file extension must be ".log"                                  #
#     -Lines 52 and 53 produce an output text file that contains     #  
#     all lines that were matched and remove from the log file.      #
#     If the output file is not wanted, comment out or delete        #
#     these lines                                                    #
#                                                                    #
######################################################################



files = Path(".").glob("*.txt")

pattern = re.compile(r'(^sho?w? run.*|^Building config|^\.\.\.|^platform|^service (call|timestamps)|^Current config|^version \d+\.\d+|^boot-|'
                    r'^no aaa new|^call-|^ mode none| *!( *\w)?|^ contact-email|^ profile "| *(no)?destination transport|'
                    r'^login on|^subscriber t|^multilink b|^crypto pki (certificate|trustpoint)|^ enrollment|^ subject-name|'
                    r'^ revocation-check|^ rsakeypair TP|^ certificate|^no license|^license|^memory free|^diagnostic bootup|'
                    r'^ip (http|tftp source-|forward-pro)|^control-plane|^line aux|^diagnostic|^ stopbits \d+|^no service|'
                    r'^no aaa|^no device-tracking|^memory free|^redundancy|^ mode sso|^transceiver type|^ monitoring|'
                    r'^class-map match-any (system-cpp-(police|default)|non-client-nrt)|^  description (EWLC (Control|Data,)|'
                    r'Topology control|Sw forwarding, L2|Openflow, Exc|Punt Webauth|L2 (LVX)? ?control|'
                    r'Forus Address resolution and Forus traffic|MCAST END STATION|High Rate App|DOT1X Auth|ICMP redirect, ICMP_GEN|'
                    r'Protocol snooping|DHCP snooping|System Critical|ICMPGEN,B)|^  active|^policy-map system-cpp|'
                    r'Stackwise Virtual|Routing control and Low Latency|^ service-policy input system-cpp|^switch 1 provision)[-\w\s]+')

exclamation = re.compile(r' ?!()')

files = Path(".").glob("*.log")
files_to_trim = []
file_names = []
match_log = re.compile(r'log$')

for file in files:
  result = re.search(match_log, file.name)
  if str(type(result))=='<class \'NoneType\'>':
    pass
  elif str(type(result))=='<class \'re.Match\'>':
    file_names.append(file.name[0:-4])
    files_to_trim.append(file)

for file in files_to_trim:
  wanted_commands = [] 
  with open(file.name, 'r') as f:
      for line in f.readlines():
          result = re.search(pattern, line)
          if str(type(result))=='<class \'NoneType\'>':
            wanted_commands.append(line)
          elif str(type(result))=='<class \'re.Match\'>':
            # The two lines below are here to make an output of matches, delete or comment out if matches file not wanted.
            matches = open("Matches.txt", "a")
            matches.write(line)
            pass

  for command in wanted_commands:
      command.strip()

  with open(file_names[0]+'_trimmed.log', 'w') as new_file:
      for command in wanted_commands:
          new_file.writelines(command)

  with open(file_names[0]+'_trimmed.log', 'r') as new_file: 
      trimmed_commands = new_file.readlines()

  out = ''
  for line in trimmed_commands:
    if line[0] == ' ' or line[0]=='  ' or line[0]=='   ':
      out += line
    else:
      out += f'!\n{line}'

  with open(file_names[0]+'_trimmed.log', 'w') as out_file:
    if out[0] == '\n':
      out_file.write(out[1: ])
    else:
      out_file.write(out)
  file_names.pop(0)