include "base.thrift"

service AccountService {
  base.StatusResponse addAccount(1:AddAccount addAccount)
}

struct AddAccount {
  1: required i64 id,
  2: required string currencySymbol,
  3: required base.Genre genre,
  4: required base.AccountType accountType,
  5: required i32 pairId
}
