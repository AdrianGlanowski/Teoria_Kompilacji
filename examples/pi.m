pi = 0.0;
n = 1;
for i = 1:1000 {
    pi += 4.0 / n - 4.0 / (n + 2);
    n += 4;
}
print pi;
