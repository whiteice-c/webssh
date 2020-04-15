### 环境

python3.6 、 Django==2.1.4 、dwebsocket==0.5.10 、paramiko==2.4.2

### 快速安装

1、使用conda创建python环境

``$ conda create -n webssh python = 3.6   ``

2、进入创建的环境

`` $ source activate webssh ``

3、 使用pip安装所需依赖

`` $ pip install -r requirements.txt ``

### 错误记录：

- raise NoValidConnectionsError(errors) paramiko.ssh_exception.NoValidConnectionsError: [Errno None] Unable to connect to port 22 on 127.0.0.1 or ::1

  错误出现在客户端向服务器断建立socket通信请求后，后台收到请求信息后无法通过ssh连接服务器端，原因就是linux下未启动sshd服务。

  **解决办法 : ** 输入 ``$ rcsshd start ``  启动sshd服务（opensuse系统下，其他系统需自行查找命令），若提醒没有sshd，则需安装sshd服务。  

### 引用：

[1]: https://www.cnblogs.com/xiao987334176/p/10289262.html	"“实现web页面执行命令并实时输出”"

