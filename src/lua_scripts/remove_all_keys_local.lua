local get_count_keys = tonumber(ARGV[1]) == 1
local key_count

if get_count_keys then
    key_count = redis.call("DBSIZE")
end

redis.call("FLUSHDB")

return key_count