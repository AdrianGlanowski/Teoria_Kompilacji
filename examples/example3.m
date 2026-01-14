# control flow instruction

N = 4;
M = 20;

X = zeros(7);

X[4, 6] = 12;

if(N==10)
    print "N==10";
else if(N!=10)
    print "N!=10";


if(N>5) {
    print "N>5";
}
else if(N>=0) {
    print "N>=0";
}

if(N<10) {
    print "N<10";
}
else if(N<=15)
    print "N<=15";

k=15;

while(k>10)
    k = k - 1;

while(k>0) {
    if(k<5)
        i = 3;
    else if(k<10)
        i = 4;   
    else
        i = 5;
    
    k = k - 1;
}


for i = 4:N
  for j = i:M
    print i, j;

for i = 1:N {
    if(i<=N/16)
        print i;
    else if(i<=N/8)
        break;
    else if(i<=N/4)
        continue;
    else if(i<=N/2)
        return 7;
}
