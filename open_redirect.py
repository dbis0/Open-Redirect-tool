import optparse
import colorama
import requests
import urllib
from urlparse import urlparse 
from colorama import Fore, Style
from goop import goop

def search(domain, dorks, verbios):
    domain = domain
    dorks = open(dorks, "r")
    payloads = dorks.readlines()
    final = []
    print(Fore.CYAN+"[*] Scanning is established, it may takes a minutes ...\n\n")
    for payload in payloads:
        dork = "site:"+domain+" AND inurl:"+payload
        result = goop.search(dork, cookies, page=10, full=True)
        print(Fore.MAGENTA+"[+] Trying: "+dork)
        if result:
            for each in result: 
                final.append(str(result[each]['url']))
        if verbios and not result:
            print(Fore.RED+"[-] No result for this dork >> "+dork)
    print(Fore.GREEN+"[+] Scanning Done \n")
    dorks.close()
    if len(final) == 0:
        print(Fore.RED+"[-] No result for your scan, Try Harder! U can Do it")
    else:
        x=1
        for i in final:
            if(CheckInterest(i)):
                print(Fore.YELLOW+"["+str(x)+"] "+"Interesting one >> "+ i + "\n")
                x=x+1
            else:
                print(Fore.BLUE+"["+str(x)+"] "+i+"\n")
                x=x+1


def CheckInterest(checkit):
    white_list = ['=http','%3dhttp','%3dhttps','=https','%3D%2F','=/']
    for i in white_list:
        if i.lower() in checkit.lower():
            checkVuln(checkit)
            return True
    return False

def checkVuln(Interst):
    pre = urllib.unquote(Interst)
    vuln = urllib.unquote(pre)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(vuln, headers=headers)
    original = urlparse(vuln).netloc
    actual = urlparse(r.url).netloc
    if(r.status_code == 200 and (vuln != r.url)):
        print(Fore.RED+'Mostly Vulnerable !!!! >>>>>'+vuln)
        print(Fore.RED+'cuz it comes from '+original+' goes to --> '+actual+"\n")

def banner():
    schizo="""                        ,---,                                     
                      ,--.' |      ,--,                           
                      |  |  :    ,--.'|          ,----,   ,---.   
  .--.--.             :  :  :    |  |,         .'   .`|  '   ,'\  
 /  /    '     ,---.  :  |  |,--.`--'_      .'   .'  .' /   /   | 
|  :  /`./    /     \ |  :  '   |,' ,'|   ,---, '   ./ .   ; ,. : 
|  :  ;_     /    / ' |  |   /' :'  | |   ;   | .'  /  '   | |: : 
 \  \    `. .    ' /  '  :  | | ||  | :   `---' /  ;--,'   | .; : 
  `----.   \'   ; :__  |  |  ' | :'  : |__   /  /  / .`||   :    | 
 /  /`--'  /'   | '.'||  :  :_:,'|  | '.'|./__;     .'  \   \  /  
'--'.     / |   :    :|  | ,'    ;  :    ;;   |  .'      `----'   
  `--'---'   \   \  / `--''      |  ,   / `---'                   
              `----'              ---`-'                          
                                                                  """
    twitter="twitter:@isch1zo"
    new_line="----------------------------------------------------------------------------------------------------"
    print(Fore.BLUE+"\n"+schizo)
    print(Fore.RED+twitter)
    print(Fore.WHITE+new_line)

def get_arguments():
    banner()
    parser = optparse.OptionParser()
    parser.add_option("-d", "--domain", dest="domain", help="Enter Target Domain")
    parser.add_option("-f", "--dorks", dest="dorks", help="Enter Dorks")
    parser.add_option("-v", "--verbose", dest="verbose", help="Print more data", action="store_true")
    #Verbose
    (options, arguments) = parser.parse_args()
    if not options.domain:
        parser.error("[-] Please specify a domain, use --help for more info.")
    elif not options.dorks:
        parser.error("[-] Please specify a dorks file, use --help for more info.")
    else:
        return options


cookies = "c_user=XXXXXXXXXXXXXXX; xs=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX;"
options = get_arguments()
search(options.domain, options.dorks, options.verbose)
