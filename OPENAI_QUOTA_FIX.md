# Fixing OpenAI API Quota Error

## Error Message
```
Error code: 429 - You exceeded your current quota, please check your plan and billing details.
```

## What This Means

You've hit one of these limits:
1. **No payment method added** - Free tier credits exhausted
2. **Quota exceeded** - Monthly or rate limits reached
3. **Billing not configured** - Account needs payment setup

## Solutions

### Solution 1: Add Payment Method (Most Common)

1. Go to [OpenAI Billing](https://platform.openai.com/account/billing)
2. Click **"Add payment method"**
3. Enter your credit card details
4. Confirm the payment method
5. Wait a few minutes for the system to update

### Solution 2: Check Your Usage

1. Visit [OpenAI Usage Dashboard](https://platform.openai.com/usage)
2. Review:
   - Current usage vs. limits
   - Rate limits (requests per minute)
   - Monthly spending limits

### Solution 3: Upgrade Your Plan

1. Go to [OpenAI Settings](https://platform.openai.com/account/limits)
2. Check tier limits:
   - **Tier 1 (Default)**: $0.002/1K tokens for GPT-3.5
   - Higher tiers: Higher rate limits
3. Request tier increase if needed

### Solution 4: Wait for Reset

- Rate limits reset immediately (per minute/hour)
- Usage limits reset monthly
- Check when your limit resets in the dashboard

## Verify Your Setup

1. **API Key is Valid**
   ```bash
   # Test your API key (replace YOUR_KEY)
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_KEY"
   ```

2. **Check Account Status**
   - Visit: https://platform.openai.com/account
   - Ensure account is active and in good standing

3. **Verify Billing**
   - Payment method is active
   - No outstanding payments
   - Account has available credit

## Alternative: Use Different Models

If quota issues persist, you can modify the model settings in `config.py`:

```python
# Use cheaper model
EMBEDDING_MODEL = "text-embedding-ada-002"  # Older, cheaper
LLM_MODEL = "gpt-3.5-turbo"  # Already the cheapest option
```

## Cost Estimation

For this chatbot:
- **Embeddings**: ~$0.0001 per 1K tokens
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens

**Typical usage:**
- Creating knowledge base (1 document): ~$0.01-0.05
- Each query: ~$0.001-0.01

## Still Having Issues?

1. **Check OpenAI Status**: https://status.openai.com/
2. **Contact OpenAI Support**: https://help.openai.com/
3. **Review API Documentation**: https://platform.openai.com/docs/guides/error-codes

## Quick Checklist

- [ ] Payment method added to OpenAI account
- [ ] Payment method is active and verified
- [ ] Account has available credit/budget
- [ ] API key is valid and has correct permissions
- [ ] Not exceeding rate limits (requests per minute)
- [ ] Monthly usage limit not exceeded
- [ ] Account is in good standing (no suspensions)

Once you've resolved the billing/quota issue, refresh the Streamlit app and try creating the knowledge base again.

