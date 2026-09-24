# Router Policy
1. If prompt OR context hits redaction patterns -> LOCAL only.
2. Structured/deterministic tasks (finance, tax math) -> send schema only,_daily raw numbers.
3. Cost guard: skip cloud if projected spend > max_daily_spend_usd.
4. Cloud allowed only when privacy==low and local router confidence < 0.6.
