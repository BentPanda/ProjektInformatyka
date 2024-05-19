import subprocess
import sys
import json
from colorama import Fore, Style

def audit_security(file_path):
    result = subprocess.run(['bandit', '-q', '-ll', '-f', 'json', file_path], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(Fore.GREEN + "Wyniki audytu bezpieczeństwa:" + Style.RESET_ALL)
        try:
            parsed_result = json.loads(result.stdout)
            if parsed_result['results']:
                for issue in parsed_result['results']:
                    print(Fore.YELLOW + "Problem znaleziony w pliku: " + Fore.CYAN + "{}".format(issue['filename']) + Style.RESET_ALL)
                    print("Opis problemu: " + issue['issue_text'])
                    print("Zakres linii: {} do {}".format(issue['line_range'][0], issue['line_range'][-1]))
                    print("Poziom zagrożenia: {}, Pewność: {}".format(issue['issue_severity'], issue['issue_confidence']))
                    print("Link do szczegółów CWE: " + issue['issue_cwe']['link'])
                    print("Więcej informacji: " + issue['more_info'])
                    print("Fragment kodu: \n" + issue['code'].replace('\\n', '\n'))
                    print("\n" + "-"*60 + "\n")
            else:
                print(Fore.YELLOW + "Nie znaleziono problemów bezpieczeństwa." + Style.RESET_ALL)
        except json.JSONDecodeError:
            print(Fore.RED + "Nie udało się przetworzyć wyników jako JSON." + Style.RESET_ALL)
            print(result.stdout)
    else:
        print(Fore.YELLOW + "Nie znaleziono problemów bezpieczeństwa." + Style.RESET_ALL)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(Fore.RED + "Użycie: python audit_script.py [ścieżka_do_pliku]" + Style.RESET_ALL)
        sys.exit(1)
    
    file_path = sys.argv[1]
    audit_security(file_path)
