import paramiko
import os
import argparse
import sys
import traceback


def execute_sshcommand(ssh,cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.readlines()
    error = stderr.readlines()

    if error:
        print("[+] Error: " + str(error) + '\n')
        raise

    return output

def get_app_path(output):

    temp_path = ''
    if output:
        for i in output:
            if '/var/' in i:
                temp_path = i
                break

    if temp_path == '':
        print("[+] Error : App not running \n")
        raise

    for path in temp_path.split():
        if '/var/' in path:
            app_path = path + '/'
            break

    temp = app_path.split('/')
    for i in range(0,len(temp)):
        if len(temp[i]) > 20:
            break

    temp = temp[1:i+1]
    app_path = '/' + str('/'.join(temp)) + '/'

    return app_path

def get_dotapp_folder_path(output):

    dotapp_folder = ''

    if output:
        for i in output:
            if '.app' in i:
                dotapp_folder = i
                break

    if dotapp_folder == '':
        print("[+] Not able to collect '.app' folder path \n")
        raise

    dotapp_folder = dotapp_folder.strip()
    dotapp_folder = '"' + dotapp_folder + '"'

    dotapp_folder_path = app_path + dotapp_folder

    return dotapp_folder_path



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='xIPA - By Mr. Sup3rN0va')
    parser.add_argument('-o', '--output', dest='output_ipa', help='Specify name of the decrypted IPA')
    parser.add_argument('-H', '--host', dest='ssh_host', help='Specify SSH hostname')
    parser.add_argument('-P', '--port', dest='ssh_port', help='Specify SSH port')
    parser.add_argument('-u', '--user', dest='ssh_user', help='Specify SSH username')
    parser.add_argument('-p', '--password', dest='ssh_password', help='Specify SSH password')
    parser.add_argument('target', nargs='?', help='Bundle identifier or display name of the target app')

    args = parser.parse_args()

    if not len(sys.argv[1:]):
        parser.print_help()
        sys.exit(1)

    # Checking SSH Arguments

    if args.ssh_host:
        host = args.ssh_host
    else:
        print("[-] IP to SSH is must. Check HELP")
        parser.print_help()
        sys.exit(1)

    if args.ssh_port:
        port = int(args.ssh_port)
    else:
        print("[+] SSH port not set. Using Default : 22")
        port = 22

    if args.ssh_user:
        username = str(args.ssh_user)
    else:
        print("[+] SSH username not set. Using Default : root")
        username = 'root'
                        
    if args.ssh_password:
        password = str(args.ssh_password)
    else:
        print("[+] SSH password not set. Using Default : alpine")
        password = 'alpine'

    # Checking IPA Extraction Arguments

    if args.target:
        app_search_name = str(args.target)
    else:
        print("[-] Source app name is must. Check HELP")
        parser.print_help()
        sys.exit(1)

    if args.output_ipa:
        extracted_ipa_name = str(args.output_ipa)
    else:
        print("[-] Output IPA name is must. Check HELP")
        parser.print_help()
        sys.exit(1)  

    # Initiating SSH

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port, username, password)

        print("[+] Connected to iDevice")

    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print("[-] Got Exception: No Valid Connection ::: " + str(e))
        print('[-] Try specifying -H/--hostname and/or -p/--port')
        sys.exit(1)

    except paramiko.AuthenticationException as e:
        print("[-] Got Exception: Authentication Error ::: " + str(e))
        print('[-] Try specifying -u/--username and/or -P/--password')
        sys.exit(1)

    except Exception as e:
        print('[-] Caught Exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        sys.exit(1)

    # COMMAND 1 - Get APP Path

    cmd = 'ps -ax | grep ' + app_search_name

    try:
        output = execute_sshcommand(ssh_client, cmd)
        app_path = get_app_path(output)

        print("[+] Got Application Installation Folder")

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        print("\n[+] Closing the connection")

        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    # COMMAND 2 - Get DOTAPP Folder Path

    cmd = 'ls ' + app_path

    try:
        output = execute_sshcommand(ssh_client, cmd)
        dotapp_folder_path = get_dotapp_folder_path(output)

        print("[+] Got App Folder to extract IPA")

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        print("\n[+] Closing the connection")

        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    # Extracting IPA from iDevice

    payload_path = app_path + 'Payload/'
    print("[+] Extracting IPA of the Application")

    try:
        cmd = 'mkdir -p ' + payload_path
        output = execute_sshcommand(ssh_client, cmd)

        cmd = 'cp -rf ' + dotapp_folder_path + ' ' + payload_path
        output = execute_sshcommand(ssh_client, cmd)

        cmd = 'zip -9rq ' + app_path + '/Payload.zip ' + payload_path
        output = execute_sshcommand(ssh_client, cmd)

        cmd = 'mv -f ' + app_path + '/Payload.zip ' + app_path + extracted_ipa_name
        output = execute_sshcommand(ssh_client, cmd)

        cmd = 'rm -rf ' + payload_path
        output = execute_sshcommand(ssh_client, cmd)

        print("[+] Created IPA of the Application")

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        print("\n[+] Closing the connection")

        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    # Get IPA File to Desktop

    sftp_from = app_path + extracted_ipa_name

    try:
        sftp = ssh_client.open_sftp()
        sftp.get(sftp_from, extracted_ipa_name)

        print("[+] Successfully downloaded IPA to current folder")

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        if sftp:
            sftp.close()

        print("\n[+] Closing the connection")

        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    if sftp:
        sftp.close()

    # Delete the IPA file from iDevice

    cmd = 'rm -rf ' + app_path + extracted_ipa_name

    try:
        output = execute_sshcommand(ssh_client, cmd)

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        print("\n[+] Closing the connection")
        
        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    # Re-Align downloaded IPA for re-installation

    new_app_path = os.getcwd() + app_path
    print("[+] Re-aligning downloaded IPA for re-installation")
    
    cmd = '/bin/bash alignIPA ' + new_app_path + ' ' + extracted_ipa_name

    try:
        os.system(cmd)

        print("[+] IPA re-aligned. Can be used for re-installation")

    except Exception as e:
        print('[-] Caught Exception: %s %s' % (e.__class__, e))
        traceback.print_exc()

        print("[-] Downloaded IPA needs to be aligned manually")
        print("\n[+] Closing the connection")

        if ssh_client:
            ssh_client.close()
        sys.exit(1)

    print("[+] Closing the connection")

    if ssh_client:
        ssh_client.close()

    print("[+] All tasks completed\n\n")

    print("[+] IPA Extracted : " + os.path.join(os.getcwd(), extracted_ipa_name))

    sys.exit(0)

