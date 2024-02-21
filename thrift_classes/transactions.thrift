service TransactionService {
  StatusResponse submitTransaction(1:TransactionBulk transactionBulk)
}

struct Empty {}

struct Transaction {
  1: i64 number,
  2: double amount,
  3: double freezeAmount,
  4: string currency,
  5: string entity,
  6: string subsidiaryAccount,
  7: i32 entityType,
  8: double minAmount,
  9: string description
}

struct TransactionBulk {
  1: string uniqueId,
  2: i64 timestamp,
  3: i64 objectId,
  4: string eventType,
  5: list<Transaction> transactions
}

struct StatusResponse {
  1: i32 status,
  2: string message
}
