# test_pycaching.py
import pycaching

print("pycaching version:", pycaching.__version__)

# Try to create a client (this is the first step)
client = pycaching.Geocaching()

print("✅ Client created successfully!")
print("Now we need to test login...")