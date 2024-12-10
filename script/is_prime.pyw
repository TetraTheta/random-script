import sys
import tkinter.messagebox as msgbox

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

try:
    number = int(sys.argv[1])  # Convert the input to an integer
except ValueError:
    msgbox.showerror("ERROR", "Please provide a valid integer.")
    sys.exit(1)

if is_prime(number):
    msgbox.showinfo("YES", f"{number} is a Prime Number")
else:
    msgbox.showwarning("NO", f"{number} is NOT a Prime Number")
