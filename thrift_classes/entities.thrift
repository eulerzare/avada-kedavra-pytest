include "base.thrift"

service EntityService {
  GetEntitiesAccountsResponse getEntitiesAccounts(1: RequestGetEntityAccount requestGetEntityAccount)
}

struct RequestGetEntityAccount {
  1: required list<i64> uniqueIds
}

struct EntityAccount {
  1: i64 uniqueId
  2: base.Currency currency
  3: base.Genre genre,
  4: base.AccountType accountType,
  5: string balance,
  6: string freezeBalance,
  7: string minBalance,
}

struct GetEntitiesAccountsResponse {
  1: i32 status,
  2: string message,
  3: list<EntityAccount> entityAccount
}