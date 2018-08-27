require 'sinatra'
require 'sinatra/json'
require 'rack/contrib'
require 'dry-validation'
require 'dalli'
require 'http'

require 'time'
require 'json'
require 'yaml'

require './helpers'
class Sinatra::Base
  use Rack::PostBodyContentTypeParser
  configure do
    set :lfg_hook, ENV['LFG_HOOK']
    set :gb_webhooks, YAML.load_file('config/gb_webhooks.yml')

    set :mutex, Thread::Mutex.new
    set :cache, Dalli::Client.new(
      ENV['MEMCACHE_SERVER'] || 'localhost:11211',
      username: ENV['MEMCACHE_USERNAME'],
      password: ENV['MEMCACHE_PASSWORD'],
      namespace: 'tera_lab',
      compress: true
    )
  end

  helpers do
    def validates(code=412, &blk)
      schema = Dry::Validation.Schema(&blk)
      validation = schema.call(params)
      halt(
        code,
        {'Content-Type' => 'application/json'},
        validation.errors.to_json
      ) if validation.failure?
    end
  end
end

require './controllers/lfg'
require './controllers/guild_bam'

class App < Sinatra::Base
  get '/' do
    return 'ok'
  end

  use LfgController
  use GuildBamController
end


