# Finance Backend

A Python-based backend service that provides AI-powered financial analysis and advice through multiple specialized agents. This service integrates with the Fi Money MCP server to access real financial data and provides comprehensive financial insights.

## Features

- **Multi-Agent Architecture**: Specialized agents for different financial domains
- **Fi Money Integration**: Real-time access to user financial data via MCP protocol
- **Tax Advisory**: Indian tax law expertise and optimization strategies
- **Investment Analysis**: Mutual fund, stock, and bond comparison tools
- **Market Data**: Real-time financial market information
- **File Upload Support**: Process financial documents and statements

## Architecture

### Agent System

- **PersonalFinanceAgent**: Root agent coordinating all financial queries
- **TaxAdvisorAgent**: Specialized in Indian tax regulations
- **SearchAgent**: Internet search for financial and market data
- **InvestmentComparisonAgent**: Analysis and ranking of investment options
- **Fi Money MCP Agent**: Direct integration with Fi Money platform

### Technology Stack

- **Framework**: FastAPI
- **AI Model**: Gemini 2.5 Pro
- **MCP Integration**: Async MCP client for Fi Money data
- **File Processing**: Support for PDF, DOC, images

## Project Structure

```
Finance-backend/
├── app/
│   ├── agent/
│   │   └── finance_agent/
│   │       ├── agent.py              # Main agent configuration
│   │       ├── prompt.py             # Agent prompts and instructions
│   │       └── tools/
│   │           └── fi_money_mcp.py   # Fi Money MCP integration
│   ├── data/                         # Sample data files
│   │   ├── credit_report.json
│   │   ├── epf_details.json
│   │   └── net_worth.json
│   └── main.py                       # FastAPI application entry point
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Container configuration
└── README.md                         # This file
```

## API Endpoints

### Agent Query

- **POST** `/agent/query`
  - Process user queries with optional file uploads
  - Parameters: `user_id`, `session_id`, `message`, `file` (optional)
  - Returns: AI-generated financial advice and analysis

## Environment Variables

```bash
MCP_URL=http://localhost:8080  # Fi Money MCP server URL
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Fi Money MCP server running (see fi-mcp-dev)

### Local Development

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Set environment variables**:

```bash
export MCP_URL=http://localhost:8080
```

3. **Run the server**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment

```bash
docker build -t finance-backend .
docker run -p 8000:8000 -e MCP_URL=http://mcp:8080 finance-backend
```

## Usage Examples

### Basic Query

```bash
curl -X POST "http://localhost:8000/agent/query" \
  -F "user_id=user123" \
  -F "session_id=session456" \
  -F "message=What is my current net worth?"
```

### Query with File Upload

```bash
curl -X POST "http://localhost:8000/agent/query" \
  -F "user_id=user123" \
  -F "session_id=session456" \
  -F "message=Analyze my bank statement" \
  -F "file=@statement.pdf"
```

## Agent Capabilities

### Financial Analysis

- Net worth calculation and tracking
- Investment portfolio analysis
- Cash flow analysis
- Debt management advice

### Tax Optimization

- Section 80C deductions
- Tax-saving investment recommendations
- Capital gains analysis
- Tax liability calculations

### Investment Advisory

- Mutual fund comparisons
- Stock analysis and recommendations
- Bond and FD comparisons
- Risk assessment and portfolio optimization

### Market Intelligence

- Real-time market data
- Financial news and analysis
- Economic indicators
- Sector performance insights

## Integration with Fi Money

The backend integrates with Fi Money MCP server to access:

- Bank account balances and transactions
- Mutual fund holdings and performance
- EPF account details
- Credit report and loan information
- Investment portfolio data

## Error Handling

The service includes comprehensive error handling for:

- MCP server connectivity issues
- Invalid user sessions
- File processing errors
- AI model failures

## Security

- Session-based authentication
- File upload validation
- Input sanitization
- Secure MCP communication

## Development

### Adding New Agents

1. Create agent class in `app/agent/`
2. Define prompts in `prompt.py`
3. Register agent in `agent.py`
4. Add tools if needed

### Testing

```bash
# Run tests (when available)
pytest tests/
```

## Troubleshooting

### Common Issues

1. **MCP Connection Failed**: Ensure Fi Money MCP server is running
2. **File Upload Errors**: Check file size and format restrictions
3. **Agent Timeout**: Increase timeout settings for complex queries

### Logs

Check application logs for detailed error information:

```bash
docker logs finance-backend
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

[Add your license information here]
