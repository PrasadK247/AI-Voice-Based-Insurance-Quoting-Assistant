# User Flow – UC189

## Primary Flow: Get Insurance Quote via Voice

```
┌──────────┐     ┌──────────────┐     ┌──────────────────┐
│ Customer │────>│ Open Web App │────>│ Click Microphone │
└──────────┘     └──────────────┘     └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ Speak Requirements│
                                      │ "I need health   │
                                      │ insurance for my │
                                      │ family of 4"     │
                                      └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ AI Asks Follow-up│
                                      │ Questions:       │
                                      │ - Age, income    │
                                      │ - Pre-conditions │
                                      │ - Budget         │
                                      └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ AI Generates     │
                                      │ Profile + Risk   │
                                      │ Assessment       │
                                      └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ Shows Recommended│
                                      │ Policies + Quotes│
                                      └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ Customer Compares│
                                      │ & Selects Policy │
                                      └────────┬─────────┘
                                               │
                                      ┌────────▼─────────┐
                                      │ Call Summary     │
                                      │ Generated & Saved│
                                      └──────────────────┘
```

## Alternative Flows
1. **Text-based input:** Customer types requirements instead of speaking into the microphone.
2. **Returning customer:** Voice biometrics identify customer and load existing profile.
3. **Policy comparison:** Customer asks to compare specific plans side by side.
4. **Multilingual:** Customer speaks in supported languages (Spanish, German, French, etc.).
