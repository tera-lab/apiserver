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
  set :mutex, Thread::Mutex.new
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

class String
  require 'nkf'

  def normalize
    NKF.nkf('-w --hiragana', self.downcase)
  end
end

get '/' do
  'ok'
end

post '/party_match_link' do  
  validates do
    configure do
      def self.messages
        super.merge(
          en: {errors: {
            not_spam_user: 'he is spam user',
            not_spam_message: 'message contains spam word'
          }}
        )
      end
    end
  
    required(:playerId).filled(:int?, gt?: 0)
    required(:lfg).schema do
      required(:id).filled(:int?, gt?: 0)
      required(:unk2).value(eql?: 65)
      required(:name).filled(:str?)
      required(:message).filled(:str?)

      validate(not_spam_user: :name) do |name|
        name.normalize != 'あるていしあ' &&
        name.normalize !~ /^知.+ちゃん$/
      end

      validate(not_spam_message: :message) do |_|
        message = _.normalize
        ['砲火', '名誉', '闘志', '回収', '海賊'].none?{|word| message.include?(word)}
      end
    end
  end

  lfg = params[:lfg]
  settings.mutex.synchronize do
    last_pr = settings.cache.get(lfg['id'])
    halt 429 if last_pr && lfg['message'] == last_pr
    settings.cache.set(lfg['id'], lfg['message'], 180)
  end

  color = lfg['raid'] == 0 ? 0x54a0ff : 0xfeca57
  color = 0xee5253 if lfg['message'] =~ /買い?取/

  HTTP.post(settings.lfg_hook, json: {
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