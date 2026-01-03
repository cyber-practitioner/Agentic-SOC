# AI-Powered Security Operations Center (SOC) Assistant

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production-brightgreen.svg)]()

An intelligent Security Operations Center assistant that automates threat detection, alert analysis, and incident response workflows. This solution integrates AI-driven decision making with traditional SIEM platforms to provide automated security orchestration and response capabilities.

## Overview

The AI SOC Assistant processes security alerts from SIEM platforms, performs intelligent analysis using large language models, and executes automated response actions through integration with security orchestration platforms. The system is designed for organizations implementing security automation using modern no-code/low-code approaches.

### Key Features

- **Automated Alert Processing**: Ingests and analyzes security alerts from multiple SIEM platforms
- **AI-Powered Analysis**: Leverages large language models for threat assessment and recommendation generation
- **Workflow Automation**: Executes security playbooks and response actions automatically
- **Real-time Dashboard**: Provides operational visibility into security events and automated responses
- **Multi-platform Integration**: Supports integration with Splunk, Tines, and other security platforms

## Architecture

The system consists of four core components:

1. **AI Agent** (`agent.py`) - Processes alerts and generates security recommendations
2. **Web Server** (`webserver.py`) - Handles webhook ingestion and API endpoints
3. **Automation Engine** - Executes security playbooks via Tines integration
4. **Dashboard Interface** - Provides real-time operational visibility

## System Requirements

- **Memory**: Minimum 20GB RAM (for local LLM deployment)
- **Python**: Version 3.8 or higher
- **Dependencies**: Ollama, LangChain, FastAPI, Tines API access
- **Network**: Secure external access via ngrok or similar tunneling solution

## Quick Start

### Prerequisites

Ensure you have the following components configured:

- Security automation platform (Tines) with API access
- SIEM platform (Splunk) with webhook capability
- External access endpoint (ngrok)
- LangChain API credentials
- Ollama model server

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Agentic-SOC
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the System

Start the required services in separate terminals:

```bash
# Terminal 1: Start the AI agent
python3 agent.py

# Terminal 2: Start the web server
python3 webserver.py

# Terminal 3: Start ngrok tunnel
ngrok http 8000

# Terminal 4: Start Ollama model server
ollama serve
```

## Configuration

### Environment Variables

```bash
# API Keys
LANGCHAIN_API_KEY=your_langchain_api_key
TINES_API_KEY=your_tines_api_key

# Service Endpoints
NGROK_SERVER=https://your-ngrok-url.ngrok.io
TENANT_DOMAIN=your-tines-domain

# SIEM Configuration
SPLUNK_HOST=your-splunk-server
SPLUNK_PORT=8089
```

### SIEM Integration

Configure your SIEM platform to send alerts to:
```
https://your-ngrok-url.ngrok.io/splunk-webhook
```

## Security Considerations

- Implement proper authentication for all API endpoints
- Use HTTPS for all external communications
- Regularly audit automation workflows and access controls
- Monitor all agent activities and maintain comprehensive logs
- Ensure secure storage of API keys and credentials

## Project Structure

```
Agentic-SOC/
├── agent.py              # AI agent implementation
├── webserver.py          # FastAPI webhook receiver
├── tooling.py            # Security automation tools
├── tines.py              # SOAR platform integration
├── use_boto3.py          # AWS security group management
├── attack_range/         # Splunk Attack Range configuration
└── wazuh-docker/         # Wazuh SIEM deployment
```

## Documentation and Media

### Architecture Diagram
View the detailed system architecture diagram:
- [Architecture Diagram (SVG)](https://github.com/cyber-practitioner/Agentic-SOC/blob/main/AI%20Assistant%20soc%20Architecture.drawio.svg)

![AI SOC Architecture](https://github.com/cyber-practitioner/Agentic-SOC/raw/main/AI%20Assistant%20soc%20Architecture.drawio.svg)

### Video Demonstration
Watch the system in action:
- [AI SOC Assistant Demo Video](https://youtu.be/EQecwdT4i7c)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit your changes (`git commit -m 'Add enhancement'`)
4. Push to the branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Support

For technical support and documentation, please refer to the project issues or contact the development team.

---

**⚠️ Security Notice**: Ensure proper security configurations are implemented before deploying in production environments.