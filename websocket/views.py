from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko

# def exec_command(comm):
#     hostname = 'localhost'
#     username = 'baibing'
#     password = '950915'
#
#     ssh = paramiko.SSHClient()
#     # 这行代码的作用是允许连接不在know_hosts文件中的主机。
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=hostname, username=username, password=password)
#     stdin, stdout, stderr = ssh.exec_command(comm)
#     result = stdout.read()
#     ssh.close()
#     return result
#
#
# @accept_websocket
# def echo_once(request):
#     if not request.is_websocket():  # 判断是不是websocket连接
#         try:  # 如果是普通的http方法
#             message = request.GET['message']
#             return HttpResponse(message)
#         except:
#             return render(request, 'index.html')
#     else:
#         for message in request.websocket:
#             message = message.decode('utf-8')
#             if message == 'backup_all':#这里根据web页面获取的值进行对应的操作
#                 command = 'sh test.sh'#这里是要执行的命令或者脚本，我这里写死了，完全可以通过web页面获取命令，然后传到这里
#                 request.websocket.send(exec_command(command))  # 发送消息到客户端
#             else:
#                 request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))

@accept_websocket
def echo_once(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')  # 接收前端发来的数据
            print(message)
            if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
                print("走到了这了")
                command = 'bash /opt/test.sh'  # 这里是要执行的命令或者脚本

                # 远程连接服务器
                hostname = 'localhost'
                username = 'root'
                password = '950915'

                print('收到请求连接消息...')
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                # result = stdout.read()
                # 循环发送消息给前端页面
                print('连接成功....')
                while True:
                    nextline = stdout.readline().strip()  # 读取脚本输出内容
                    print(nextline)
                    request.websocket.send(nextline.encode('utf-8'))  # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if not nextline:
                        break

                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))
