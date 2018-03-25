using System;
using System.Net;
using System.Net.Sockets;
using System.IO;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            using (var tcp = new TcpClient("localhost", 8800))
            {
                byte[] image = File.ReadAllBytes("../../test_images/images.jpg");
                tcp.GetStream().Write(image, 0, image.Length);
            }
        }
    }
}
