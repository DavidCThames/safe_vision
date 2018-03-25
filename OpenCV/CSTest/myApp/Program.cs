using System;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Diagnostics; 
using System.Linq;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            // full path of python interpreter  
            string python = @"C:\Python27\python.exe";  
                        
            // python app to call  
            string myPythonApp = "../../detect.py";  

            // Create new process start info 
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo(python); 
            
            // make sure we can read the output from stdout 
            myProcessStartInfo.UseShellExecute = false; 
            myProcessStartInfo.RedirectStandardOutput = true; 

            // start python app with 3 arguments  
            // 1st argument is pointer to itself, 2nd and 3rd are actual arguments we want to send 
            myProcessStartInfo.Arguments = myPythonApp;

            Process myProcess = new Process(); 
            // assign start information to the process 
            myProcess.StartInfo = myProcessStartInfo; 
            
            // start process 
            myProcess.Start();
            StreamReader myStreamReader = myProcess.StandardOutput; 
            // string myString = myStreamReader.ReadLine(); 

            //Create TCP Client
            // var tcp = new TcpClient("localhost", 8800);
            
            

            for(int i = 0; i < 6; i ++) {
                // Read the standard output of the app we called.  
                
                SendFile(i);
                string myString = myStreamReader.ReadLine(); 
                //Send the image file
                
                
                //Wait for the server to start
                
                // myString = myStreamReader.ReadLine(); 
                // myString = myStreamReader.ReadLine(); 
                            
                // // wait exit signal from the app we called 
                // myProcess.WaitForExit(); 
                
                // close the process 
                // myProcess.Close();

                // write the output we got from python app 
                myString = myStreamReader.ReadLine(); 
                Console.WriteLine("Value received from script: " + myString);  
                // myString = myStreamReader.ReadLine(); 
                // Console.WriteLine("Value received from script: " + myString); 
                
            }
            myProcess.WaitForExit(); 
            myProcess.Close();
        }

        static public void SendFile(int i) {
            using (var tcp = new TcpClient("localhost", 8800))
            {
                byte[] image = File.ReadAllBytes("../../test_images/image" + (i) + ".jpg");
                tcp.GetStream().Write(image, 0, image.Length);
                // tcp.GetStream().Flush();
            }
        }
    }
}
