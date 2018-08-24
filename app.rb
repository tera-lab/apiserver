require 'sinatra'
require 'rack/contrib'
require 'dry-validation'
require 'dalli'
require 'http'

require 'json'
require 'time'

use Rack::PostBodyContentTypeParser

configure do
  set :lfg_hook, 'https://discordapp.com/api/webhooks/482168717803782159/y6ebwOdmye9csiiusj_hJQd4cHTmNxOJ4Q7uahv9d7DMnxzn3YoBNAyy-nqlHpISJ95g'
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

get '/' do
  'ok'
end

post '/party_match_link' do  
  validates do
    required(:playerId).filled(:int?, gt?: 0)
    required(:lfg).schema do
      required(:unk2).value(eql?: 65)
      required(:message).value(
        excluded_from?: ['砲火', '名誉', '闘志', '回収', '海賊']
      )
    end
  end

  lfg = params[:lfg]
  last_pr = settings.cache.get(lfg['id'])
  halt 429 if last_pr && lfg['message'] == last_pr
  settings.cache.set(lfg['id'], lfg['message'], 60)

  color = lfg['raid'] == 0 ? 0x54a0ff : 0xfeca57
  color = 0xee5253 if lfg['message'] =~ /買い?取/

  HTTP.post(settings.lfg_hook, json:{
    embeds: [{
      author: {
        name: lfg['name']
      },
      description: lfg['message'],
      color: color,
      timestamp: Time.now.iso8601
    }]
  })
end