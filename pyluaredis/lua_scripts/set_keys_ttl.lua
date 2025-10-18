local keys = KEYS
local ttl = tonumber(ARGV[1])
local if_without_ttl = tonumber(ARGV[2]) == 1
local if_with_ttl = tonumber(ARGV[3]) == 1
local only_greater = tonumber(ARGV[4]) == 1
local only_less = tonumber(ARGV[5]) == 1
local option

if if_with_ttl then
  option = "XX"
elseif if_without_ttl then
  option = "NX"
elseif only_greater then
  option = "GT"
elseif only_less then
  option = "LT"
end

for _, key in ipairs(keys) do
  if option then
    redis.call("PEXPIRE", key, ttl, option)
  else
    redis.call("PEXPIRE", key, ttl)
  end
end