from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    clientSocket.connect((mailserver, port))

    recv = clientSocket.recv(1024).decode()
    # print(recv) #You can use these print statement to validate return codes from the server.
    # if recv[:3] != '220':
    #    print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '250':
    #    print('250 reply not received from server.')

    # Send MAIL FROM command and handle server response.
    fromCmd = 'MAIL FROM: <alice@alice.com>\r\n'
    clientSocket.send(fromCmd.encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '250':
    #    print('250 reply not received from server.')

 
    # Send RCPT TO command and handle server response.
    rcptToCmd = 'RCPT TO: <bob@bob.com>\r\n'
    clientSocket.send(rcptToCmd.encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '250':
    #    print('250 reply not received from server.')
    

    # Send DATA command and handle server response.
    dataCmd = 'DATA\r\n'
    clientSocket.send(dataCmd.encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '354':
    #    print('354 reply not received from server.')

    # Send message data.
    clientSocket.send(f"{msg}{endmsg}".encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '250':
    #    print('250 reply not received from server.')

    # Send QUIT command and handle server response.
    clientSocket.send("QUIT\r\n".encode())
    recv = clientSocket.recv(1024).decode()
    # print(recv)
    # if recv[:3] != '221':
    #    print('221 reply not received from server.')


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
