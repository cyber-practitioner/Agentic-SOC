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
- [Interactive Architecture Diagram](https://viewer.diagrams.net/index.html?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=AI%20Assistant%20soc%20Architecture.drawio.svg&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22b8UF5Q9j34Wk7VL4hwdb%22%3E5Vpbc6M2FP41nmkf4gEE2DzGtzRT70wmbrvbJ48MMlYDiAr5tr%2B%2BEkg2AnxZx3bSNp6J0UE6OpzvXIVboB9vnihMF19IgKKWZQSbFhi0LMu0HMC%2FBGVbULqKEFIcyEl7wgR%2FR5JoSOoSByjTJjJCIoZTneiTJEE%2B02iQUrLWp81JpO%2BawhDVCBMfRnXqVxywhXoKY0%2F%2FBeFwoXY2DXknhmqyJGQLGJB1iQSGLdCnhLDiKt70USSUp%2FRSrBsduLsTjKKEnbNgOiIe%2FHvkrAYmiqbD%2BVO6XT00cJGkjG2VDrI3xHzxMEYL9MiSRThB%2FZ2%2BBTGkMMCcQ59EhHJaQhK%2BtrdgccRHJr9cLzBDkxT6guea2wqnzUnCJOKmpcZyW8GVaywV1%2FEmFMbVhuvMboeULNN8y2eOeePd6Sr1xXJGyRtSIrUs0O14pueKjXAUVURdIcowh%2F0xwqHgyojYBMpRhOZMcOTy4yQc56MBMKTMTVsEMFugQD5IodEVjJZSo3%2B89CWNb4s2JcVL7J4QiRGjWz5lUTIvoKxrvbdF25M0ycZSc6THAU96g%2FSEcMd6byz8QtrLD9iOdY7tNJqLphyl%2BTGcoeiFZJjhHNcZYYzEJ6Hx%2BeaI6sbWYDigjXyrAj3Ha%2BTwgGQftuAacl9xEoigYhkTRLlkF8HYraPoVkB0dRBNA7SdG%2BEI%2Fo84%2FhphThgnyw3%2F%2BgkyBv03RH%2B%2BDE5XYVMCtKMDanfvB6h3DqANMbAWMAcD4IinPwBdNV5XYuFudVPsL6Fcw2aC%2FCXFbJsXBSLaXwIKj8U1THZVhfIyoIOiMLu%2Bi0lZUFCrNuoYkSX10bGcbdTAFHwVEoSyBQlJAqPhntrjekyCna%2Fu54yJgDLH4S%2FE2FbmY7hkREcJbTD7JpeL6z%2FFdbvjyeFgU7o32JYGL4hirkXh2wUt4Rr9Vh4UrCxHjfe88pFiJqs%2FSEPEjqnngHFQFEGGV7r%2Br4%2B0p9WjcKYgMuqAHzWVCrp5VNURqUXOqpfGOAgK8FGGv0tRhCZTghOWP7nTazmDxjyHZgtC3jjx99fx2Q7YqGO5xGjbrtXR%2FM0%2BDILk%2FSIkLU0h83nG0a%2BitBPhcuDMBoD%2B%2B2lwkkbLRKA8eR5%2BuSz5gXots8uHkg2wu4qi0p93q1BrOtcMtXULuGOoNbVQ6xyNtOcGR%2Fsjg6N5VruJ47wn78EsLXxsjjdCnb20lEn4bjjNUCm5HA2Nu%2Ba75q%2Byp%2FstxwZwgtx%2BgOOQP2SEZ%2Fw%2F9IVypgGmXCIiNDFao9k0y1uAdrYKD4TQ97UJTkOzVylgHL2AsZ1buZXC6TpuZX%2BIW6nC48FoG2ZHrz5OFR%2F5qFrKnOt0Xs02XpeJQInLGMM8QbzPK%2BOlj5TCbWmCzPL1ZCqNx3U83Xhco2ImBcfm1Y6tR3S74%2BryFWqRq66fry33X2%2BQZ5qPKppK5vPIt9lm7BpWUwPWBjqwjufcFViFxXvPJCvdKP%2BMhBSHSqNKJWWYj93uoNYUy8m3rvhOnYzWU6NAA9HhChWF%2FYGy0W5nPLnF8A3RaZyf1fNnyZNaITKCGWtKZY%2FPfCwP9y9IZJ16Iqsej1QOLW37ZokMXDNueJ84bihHKuF4k4DhmhXsOvcNGKqNvLjlVibxwS33K2JLmuR4ZMuoyNxX6LoND1gaPucDfPuuG1y1W%2FvU3ngnZ%2FQqb3%2Fc%2BzqjituXn385n8IZeak%2FJzSuFenXcEjL1h3y4TN5pHKi4%2BXXyZqnVqEcOc%2FKYIQyrm0ftffK1k63cmfNcm6SwuXp7wagPNeSBRywAtco3wDFjXn%2B12p8C9xY7NVsY0zWuYUHqCXMepSQ%2FTDlyBeGc0Gd5J58L%2Bi61TrpVi%2BRVNdxogyXUEJxLHLBq55rqalyLmKbeg%2BzK1F%2BQE18uP9xRuFd%2B5%2B4gOE%2F%3C%2Fdiagram%3E%3C%2Fmxfile%3E#%7B%22pageId%22%3A%22b8UF5Q9j34Wk7VL4hwdb%22%7D)

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