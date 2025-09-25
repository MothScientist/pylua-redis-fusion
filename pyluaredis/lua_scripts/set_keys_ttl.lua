local keys = KEYS
local ttl = tonumber(ARGV[1])

for _, key in ipairs(keys) do
    redis.call("PEXPIRE", key, ttl)
end