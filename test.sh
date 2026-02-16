# 备份原文件
cp /home/codespace/.openclaw/agents/main/agent/models.json /home/codespace/.openclaw/agents/main/agent/models.json.bak

# 写入包含 google-antigravity 的配置
cat > /home/codespace/.openclaw/agents/main/agent/models.json << EOF
{
  "providers": {
    "google-antigravity": {
      "baseUrl": "https://generativelanguage.googleapis.com",
      "models": [
        {
          "id": "gemini-3-flash",
          "name": "gemini-3-flash",
          "maxTokens": 1048576,
          "supportedFeatures": ["chat", "completion"]
        }
      ]
    },
    "github-copilot": {
      "baseUrl": "https://api.individual.githubcopilot.com",
      "models": []
    }
  }
}
EOF
