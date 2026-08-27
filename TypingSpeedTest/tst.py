# Typing Speed Test

import time

print("Welcome to the Typing Speed Test!")

sentence = "The quick brown fox jumps over the lazy dog."
print("\n Type the following sentence:")
print(sentence)

input("\n Press Enter when you're ready to start...")

start = time.time()

typed = input("\n Start typing: ")

end = time.time()

time_taken = round(end - start, 2)

speed = round(len(sentence)/time_taken, 2)

print("Time Taken: ", time_taken, "seconds")
print("Your typing speed is: ", speed, "characters per second")
