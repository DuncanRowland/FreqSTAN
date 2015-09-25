using System;
using System.Collections.Generic;
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
                  ushort id = Convert.ToUInt16(p[0]);
                  if(id>=list.Count){Console.WriteLine(-1);continue;}; 
                  jrk = new Jrk(list[id]);
                  double current = 0.0;
                  for(int i=0; i<100; i++) 
                     current += jrk.getVariables().current;
                  Console.WriteLine(current);
                  jrk.disconnect();
               }
               if(p.Length==2) {
                  ushort id = Convert.ToUInt16(p[0]);
                  if(id>=list.Count)continue;
                  ushort v = Convert.ToUInt16(Convert.ToDouble(p[1])*40.95);
                  if(v>4095)v=4095;
                  jrk = new Jrk(list[id]);
                  jrk.setTarget(v);
                  jrk.disconnect();
               }
            }
         }
      }
   }
}
