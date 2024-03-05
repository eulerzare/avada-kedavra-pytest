include "base.thrift"

service EntityService {
  AddEntityResponse addEntity(1:AddEntity addEntity)
  GetEntitiesAccountsResponse getEntitiesAccounts(1: RequestGetEntityAccount requestGetEntityAccount)
}

struct AddEntity {
  1: required string uniqueId,
}

struct AddEntityResponse {
  1: i32 status,
  2: string message,
  3: string uniqueId
}

struct RequestGetEntityAccount {
  1: required list<string> uniqueIds
}

struct EntityAccount {
  1: string uniqueId
  2: string currencySymbol
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