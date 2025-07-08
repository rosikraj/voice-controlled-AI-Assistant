import os
import site
import win32com.client
import win32com.server.register

def install():
    print("Running pywin32 post-install script...")

    try:
        import win32com
        gen_path = os.path.join(site.getsitepackages()[0], "win32com", "gen_py")
        if not os.path.exists(gen_path):
            os.makedirs(gen_path)
        print(f"Created gen_py directory at {gen_path}")
    except Exception as e:
        print(f"Error creating gen_py directory: {e}")

    try:
        print("Ensuring win32com.client and server are properly registered...")
        win32com.client.gencache.EnsureDispatch("Scripting.FileSystemObject")
        print("win32com registration complete.")
    except Exception as e:
        print(f"Error during win32com registration: {e}")

    try:
        print("Registering COM servers...")
        win32com.server.register.UseCommandLine(win32com)
    except Exception as e:
        print(f"Error registering COM servers: {e}")

if __name__ == "__main__":
    install()
