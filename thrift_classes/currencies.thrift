include "base.thrift"

service CurrencyService {
  AddCurrencyResponse addCurrency(1:AddCurrency addCurrency)
}

struct AddCurrency {
  1: required string symbol,
  2: required string name,
}

struct AddCurrencyResponse {
  1: i32 status,
  2: string message,
  3: i64 currencyId
}
