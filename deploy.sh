#!/bin/bash

# Medical Diagnosis KBS - Deployment Helper Scripts
# Choose the platform you want to deploy to

echo "=================================="
echo "Medical Diagnosis KBS Deployment"
echo "=================================="
echo ""
echo "Select deployment option:"
echo "1) Heroku (Quick & Easy)"
echo "2) Docker (Most Flexible)"
echo "3) Local Server (Testing)"
echo "4) AWS EC2 (Full Control)"
echo "5) PythonAnywhere (Python-native)"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Heroku Deployment"
        echo "=================================="
        echo ""
        echo "Prerequisites:"
        echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Have a GitHub repository ready"
        echo ""
        read -p "Have you installed Heroku CLI? (y/n): " installed
        if [ "$installed" = "y" ]; then
            echo ""
            echo "Step 1: Login to Heroku"
            heroku login
            
            echo ""
            echo "Step 2: Create Heroku app"
            read -p "Enter app name (lowercase, no spaces): " app_name
            heroku create $app_name
            
            echo ""
            echo "Step 3: Deploy"
            git push heroku main
            
            echo ""
            echo "✅ Deployment complete!"
            echo "Your app is live at: https://$app_name.herokuapp.com"
            heroku open -a $app_name
        else
            echo "Please install Heroku CLI first: https://devcenter.heroku.com/articles/heroku-cli"
        fi
        ;;
    
    2)
        echo ""
        echo "🐳 Docker Deployment"
        echo "=================================="
        echo ""
        echo "Building Docker image..."
        docker build -t medical-kbs .
        
        echo ""
        echo "Testing locally on port 5000..."
        echo "Run: docker run -p 5000:5000 medical-kbs"
        echo ""
        echo "To deploy:"
        echo "1. Create Docker Hub account: https://hub.docker.com"
        echo "2. Tag image: docker tag medical-kbs:latest yourusername/medical-kbs:latest"
        echo "3. Push: docker push yourusername/medical-kbs:latest"
        echo "4. Deploy to your cloud platform"
        ;;
    
    3)
        echo ""
        echo "🖥️  Local Server"
        echo "=================================="
        echo ""
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        echo ""
        echo "Starting server on http://localhost:5000"
        echo ""
        python server.py
        ;;
    
    4)
        echo ""
        echo "☁️  AWS EC2 Deployment"
        echo "=================================="
        echo ""
        echo "Prerequisites:"
        echo "1. Create AWS account: https://aws.amazon.com"
        echo "2. Launch EC2 instance (Ubuntu 22.04)"
        echo "3. Download and save .pem key file"
        echo "4. Configure security group (allow ports 22, 80, 443)"
        echo ""
        echo "Steps:"
        echo "1. Connect: ssh -i your-key.pem ubuntu@YOUR_INSTANCE_IP"
        echo "2. Update system: sudo apt update && sudo apt upgrade -y"
        echo "3. Install Python: sudo apt install python3 python3-pip git -y"
        echo "4. Clone repo: git clone YOUR_REPO_URL"
        echo "5. Install deps: pip3 install -r requirements.txt"
        echo "6. Run with gunicorn: gunicorn -w 4 -b 0.0.0.0:80 server:app"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed AWS EC2 instructions"
        ;;
    
    5)
        echo ""
        echo "🐍 PythonAnywhere Deployment"
        echo "=================================="
        echo ""
        echo "Steps:"
        echo "1. Sign up at https://www.pythonanywhere.com"
        echo "2. Go to 'Files' tab"
        echo "3. Upload your project files"
        echo "4. Go to 'Web' tab → Add a new web app → Flask → Python 3.10+"
        echo "5. Edit WSGI configuration file"
        echo "6. Your app will be live at: yourusername.pythonanywhere.com"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed PythonAnywhere instructions"
        ;;
    
    *)
        echo "Invalid choice. Please run script again."
        ;;
esac

echo ""
echo "=================================="
echo "Deployment Options:"
echo "- View DEPLOYMENT_GUIDE.md for detailed instructions"
echo "- View README.md for full documentation"
echo "- Questions? Check GitHub issues"
echo "=================================="
