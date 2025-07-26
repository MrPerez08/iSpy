<<<<<<< HEAD
#!/usr/bin/env python3
"""
Startup script for iSpy Conversation Analyzer
Performs system checks and launches the Flask application
"""
import sys
import os
import requests
import subprocess
import time
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from config import Config
    from app import app
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this script from the correct directory.")
    sys.exit(1)

class SystemChecker:
    """Performs startup checks for the iSpy system"""
    
    @staticmethod
    def check_python_version():
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")
        if sys.version_info < (3, 8):
            print(f"❌ Python 3.8+ required. Current version: {sys.version}")
            return False
        print(f"✅ Python {sys.version.split()[0]} - OK")
        return True
    
    @staticmethod
    def check_dependencies():
        """Check if required packages are installed"""
        print("📦 Checking dependencies...")
        required_packages = [
            'flask',
            'requests'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} - OK")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install -r requirements.txt")
            return False
        
        return True
    
    @staticmethod
    def check_ollama_service():
        """Check if Ollama service is running"""
        print("🤖 Checking Ollama service...")
        try:
            response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✅ Ollama service running at {Config.OLLAMA_BASE_URL}")
                
                # Check if the configured model is available
                models = response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if any(Config.OLLAMA_MODEL in name for name in model_names):
                    print(f"✅ Model '{Config.OLLAMA_MODEL}' is available")
                else:
                    print(f"⚠️  Model '{Config.OLLAMA_MODEL}' not found in available models:")
                    for name in model_names:
                        print(f"   - {name}")
                    print(f"\nTo install the model, run:")
                    print(f"   ollama pull {Config.OLLAMA_MODEL}")
                    
                    choice = input("\nContinue anyway? (y/N): ").lower().strip()
                    if choice != 'y':
                        return False
                
                return True
            else:
                print(f"❌ Ollama service returned status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {Config.OLLAMA_BASE_URL}")
            print("Make sure Ollama is running. Install from: https://ollama.ai")
            print("Then run: ollama serve")
            return False
        except requests.exceptions.Timeout:
            print("❌ Timeout connecting to Ollama service")
            return False
        except Exception as e:
            print(f"❌ Error checking Ollama: {e}")
            return False
    
    @staticmethod
    def check_ports():
        """Check if the configured port is available"""
        print(f"🔌 Checking port {Config.PORT}...")
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((Config.HOST, Config.PORT))
            sock.close()
            
            if result == 0:
                print(f"❌ Port {Config.PORT} is already in use")
                print(f"Change the port in config.py or stop the service using port {Config.PORT}")
                return False
            else:
                print(f"✅ Port {Config.PORT} is available")
                return True
        except Exception as e:
            print(f"⚠️  Could not check port availability: {e}")
            return True
    
    @staticmethod
    def create_directories():
        """Create necessary directories"""
        print("📁 Creating directories...")
        directories = [
            'templates',
            'static',
            'logs'
        ]
        
        for directory in directories:
            dir_path = current_dir / directory
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            else:
                print(f"✅ Directory exists: {directory}")
        
        return True
    
    @staticmethod
    def display_startup_info():
        """Display startup information"""
        print("\n" + "="*60)
        print("🕵️  iSpy Conversation Analyzer")
        print("="*60)
        print(f"Host: {Config.HOST}")
        print(f"Port: {Config.PORT}")
        print(f"Debug Mode: {Config.DEBUG}")
        print(f"Ollama URL: {Config.OLLAMA_BASE_URL}")
        print(f"Ollama Model: {Config.OLLAMA_MODEL}")
        print("="*60)
        print(f"🌐 Open your browser to: http://{Config.HOST}:{Config.PORT}")
        print("="*60)

def main():
    """Main startup function"""
    print("🚀 Starting iSpy Conversation Analyzer...")
    print("="*60)
    
    # Perform system checks
    checks = [
        SystemChecker.check_python_version,
        SystemChecker.check_dependencies,
        SystemChecker.create_directories,
        SystemChecker.check_ports,
        SystemChecker.check_ollama_service
    ]
    
    for check in checks:
        if not check():
            print("\n❌ Startup checks failed. Please fix the issues above and try again.")
            sys.exit(1)
    
    print("\n✅ All checks passed!")
    
    # Display startup information
    SystemChecker.display_startup_info()
    
    try:
        # Launch Flask application
        print("\n🔥 Starting Flask server...")
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=False  # Prevent double startup in debug mode
        )
    except KeyboardInterrupt:
        print("\n\n👋 iSpy Conversation Analyzer stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting Flask server: {e}")
        sys.exit(1)

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Startup script for iSpy Conversation Analyzer
Performs system checks and launches the Flask application
"""
import sys
import os
import requests
import subprocess
import time
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from config import Config
    from app import app
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running this script from the correct directory.")
    sys.exit(1)

class SystemChecker:
    """Performs startup checks for the iSpy system"""
    
    @staticmethod
    def check_python_version():
        """Check if Python version is compatible"""
        print("🐍 Checking Python version...")
        if sys.version_info < (3, 8):
            print(f"❌ Python 3.8+ required. Current version: {sys.version}")
            return False
        print(f"✅ Python {sys.version.split()[0]} - OK")
        return True
    
    @staticmethod
    def check_dependencies():
        """Check if required packages are installed"""
        print("📦 Checking dependencies...")
        required_packages = [
            'flask',
            'requests'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} - OK")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install -r requirements.txt")
            return False
        
        return True
    
    @staticmethod
    def check_ollama_service():
        """Check if Ollama service is running"""
        print("🤖 Checking Ollama service...")
        try:
            response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✅ Ollama service running at {Config.OLLAMA_BASE_URL}")
                
                # Check if the configured model is available
                models = response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if any(Config.OLLAMA_MODEL in name for name in model_names):
                    print(f"✅ Model '{Config.OLLAMA_MODEL}' is available")
                else:
                    print(f"⚠️  Model '{Config.OLLAMA_MODEL}' not found in available models:")
                    for name in model_names:
                        print(f"   - {name}")
                    print(f"\nTo install the model, run:")
                    print(f"   ollama pull {Config.OLLAMA_MODEL}")
                    
                    choice = input("\nContinue anyway? (y/N): ").lower().strip()
                    if choice != 'y':
                        return False
                
                return True
            else:
                print(f"❌ Ollama service returned status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {Config.OLLAMA_BASE_URL}")
            print("Make sure Ollama is running. Install from: https://ollama.ai")
            print("Then run: ollama serve")
            return False
        except requests.exceptions.Timeout:
            print("❌ Timeout connecting to Ollama service")
            return False
        except Exception as e:
            print(f"❌ Error checking Ollama: {e}")
            return False
    
    @staticmethod
    def check_ports():
        """Check if the configured port is available"""
        print(f"🔌 Checking port {Config.PORT}...")
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((Config.HOST, Config.PORT))
            sock.close()
            
            if result == 0:
                print(f"❌ Port {Config.PORT} is already in use")
                print(f"Change the port in config.py or stop the service using port {Config.PORT}")
                return False
            else:
                print(f"✅ Port {Config.PORT} is available")
                return True
        except Exception as e:
            print(f"⚠️  Could not check port availability: {e}")
            return True
    
    @staticmethod
    def create_directories():
        """Create necessary directories"""
        print("📁 Creating directories...")
        directories = [
            'templates',
            'static',
            'logs'
        ]
        
        for directory in directories:
            dir_path = current_dir / directory
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            else:
                print(f"✅ Directory exists: {directory}")
        
        return True
    
    @staticmethod
    def display_startup_info():
        """Display startup information"""
        print("\n" + "="*60)
        print("🕵️  iSpy Conversation Analyzer")
        print("="*60)
        print(f"Host: {Config.HOST}")
        print(f"Port: {Config.PORT}")
        print(f"Debug Mode: {Config.DEBUG}")
        print(f"Ollama URL: {Config.OLLAMA_BASE_URL}")
        print(f"Ollama Model: {Config.OLLAMA_MODEL}")
        print("="*60)
        print(f"🌐 Open your browser to: http://{Config.HOST}:{Config.PORT}")
        print("="*60)

def main():
    """Main startup function"""
    print("🚀 Starting iSpy Conversation Analyzer...")
    print("="*60)
    
    # Perform system checks
    checks = [
        SystemChecker.check_python_version,
        SystemChecker.check_dependencies,
        SystemChecker.create_directories,
        SystemChecker.check_ports,
        SystemChecker.check_ollama_service
    ]
    
    for check in checks:
        if not check():
            print("\n❌ Startup checks failed. Please fix the issues above and try again.")
            sys.exit(1)
    
    print("\n✅ All checks passed!")
    
    # Display startup information
    SystemChecker.display_startup_info()
    
    try:
        # Launch Flask application
        print("\n🔥 Starting Flask server...")
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=False  # Prevent double startup in debug mode
        )
    except KeyboardInterrupt:
        print("\n\n👋 iSpy Conversation Analyzer stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting Flask server: {e}")
        sys.exit(1)

if __name__ == "__main__":
>>>>>>> 5b8b1b13de22a2879096e4fd8581723f88013350
    main()