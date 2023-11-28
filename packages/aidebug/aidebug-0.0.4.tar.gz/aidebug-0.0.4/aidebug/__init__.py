def main():
    prompt = CodeDebuggerShell()
    readline.parse_and_bind("tab: complete")

    prompt.prompt = f'{Fore.GREEN}AIDebug{Fore.RESET} {Fore.YELLOW}> {Fore.RESET}'
    prompt.cmdloop(f'''{Fore.BLUE}

    █████████   █████    ██████████            █████                        
    ███░░░░░███ ░░███    ░░███░░░░███          ░░███                         
    ░███    ░███  ░███     ░███   ░░███  ██████  ░███████  █████ ████  ███████
    ░███████████  ░███     ░███    ░███ ███░░███ ░███░░███░░███ ░███  ███░░███
    ░███░░░░░███  ░███     ░███    ░███░███████  ░███ ░███ ░███ ░███ ░███ ░███
    ░███    ░███  ░███     ░███    ███ ░███░░░   ░███ ░███ ░███ ░███ ░███ ░███
    █████   █████ █████    ██████████  ░░██████  ████████  ░░████████░░███████
    ░░░░░   ░░░░░ ░░░░░    ░░░░░░░░░░    ░░░░░░  ░░░░░░░░    ░░░░░░░░  ░░░░░███
    ___________________________________________________________________███ ░███___
                                                                    ░░██████{Fore.RESET}
    {Fore.CYAN}By J. Webster-Colby\nGithub: https://github.com/00-Python{Fore.RESET}

    Type {Fore.RED}help{Fore.RESET} for a list of commands.
    ''')

if __name__ == '__main__':
    main()