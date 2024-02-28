include "base.thrift"

service TraderService {
  AddTraderResponse addTrader(1:AddTrader addTrader)
}

struct AddTrader {
  1: required string uniqueId,
}

struct AddTraderResponse {
  1: i32 status,
  2: string message,
  3: string uniqueId
}
