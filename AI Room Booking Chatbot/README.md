# 🤖 AI Room Booking Chatbot

> An intelligent chatbot powered by IBM Watson Assistant for automated room booking management

## 📱 Demo

![AI Room booking chatbot - Demo](demo.gif)

## 👨‍💻 Author

**Sunil Sharma** - Software Developer | Cloud & DevOps Enthusiast | Aspiring ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-@sunbyte16-181717?style=for-the-badge&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)

---

## 🚀 Features

- 🤖 **AI-Powered Chatbot** - Built with IBM Watson Assistant
- 📧 **Email Integration** - Automatic email notifications for booking requests
- ☁️ **Cloud-Based** - Leverages IBM Cloud Functions
- 🔒 **Secure** - Google App Password authentication
- 📱 **User-Friendly** - Intuitive conversation flow

## 🛠️ Tech Stack

- **AI/ML**: IBM Watson Assistant
- **Cloud**: IBM Cloud Functions
- **Language**: Python 3.7
- **Email**: Gmail SMTP
- **Integration**: Webhooks

---

## 📋 Setup Instructions

### Prerequisites

- IBM Cloud Account
- Google Account with 2FA enabled
- Basic understanding of cloud services

### Step-by-Step Guide

1. **📥 Clone Repository**
   ```bash
   git clone <repository-url>
   cd AI-Room-Booking-Chatbot
   ```

2. **☁️ IBM Cloud Setup**
   - Create IBM Cloud Account at [https://cloud.ibm.com/registration](https://cloud.ibm.com/registration)
   - Login at [https://cloud.ibm.com/login](https://cloud.ibm.com/login)

3. **🤖 Watson Assistant Setup**
   - Provision IBM Watson Assistant at [https://cloud.ibm.com/catalog/services/watson-assistant](https://cloud.ibm.com/catalog/services/watson-assistant)
   - Name your service and click "Create"
   - Launch Watson Assistant tool
   - Click "Create assistant" and name your assistant
   - Click "Add an actions or dialog skill"
   - Go to "Upload skill" tab and choose [skill-Room-Booking.json](skill-Room-Booking.json)

4. **⚡ Cloud Function Setup**
   - Go to [https://cloud.ibm.com/functions/actions](https://cloud.ibm.com/functions/actions)
   - Click "Create" → "Action"
   - Provide a name, leave "Enclosing Package" as default
   - Choose Python 3.7 as runtime
   - Copy code from [IBM_Cloud_Function.py](IBM_Cloud_Function.py) and paste in the text area

5. **🔐 Google Security Setup**
   - Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable 2-step verification
   - Go to "App password" under "Signing in to Google"
   - Select "Mail" as app and "Other" as device
   - Enter custom device name (e.g., "IBM Cloud Function")
   - Copy the app password

6. **🔗 Integration**
   - In IBM Cloud Function, enter the app password on line 10 of the Python code
   - Click "Endpoints" → "Enable as Web Action" and copy the URL
   - Go back to Watson Assistant → "Options > Webhooks"
   - Paste the URL (add `.json` at the end)

## 🎉 Success!

Your AI Room Booking Chatbot is now ready to handle booking requests automatically! 🚀

---

## 📁 Project Structure

```
AI-Room-Booking-Chatbot/
├── README.md                 # Project documentation
├── demo.gif                  # Demo animation
├── IBM_Cloud_Function.py     # Cloud function code
└── skill-Room-Booking.json   # Watson Assistant skill
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Created by ❤️ [Sunil Sharma](https://github.com/sunbyte16)**

[![GitHub](https://img.shields.io/badge/GitHub-@sunbyte16-181717?style=flat-square&logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)

</div>
