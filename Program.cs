using System;
using System.Text;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Text.RegularExpressions;
using System.Threading;
using Pololu.Jrk;
using Pololu.UsbWrapper;

namespace Pololu.Jrk.JrkCmd
{
   class Program
   {
      static Jrk jrk;

      static void Main()
      {
         List<DeviceListItem> list = Jrk.getConnectedDevices();
         while(true) {
            string line;
            while((line=Console.ReadLine())!=null) {
               string[] p = line.Split();
               if(p.Length==1) {
                  int id = Convert.ToInt32(p[0]);
                  jrk = new Jrk(list[id]);
                  double current = 0.0;
                  for(int i=0; i<100; i++) 
                     current += jrk.getVariables().current;
                  Console.WriteLine(current);
                  jrk.disconnect();
               }
               if(p.Length==2) {
                  int id = Convert.ToInt32(p[0]);
                  ushort v = Convert.ToUInt16(p[1]);
                  jrk = new Jrk(list[id]);
                  jrk.setTarget(v);
                  jrk.disconnect();
               }
            }
         }
      }
   }
}
