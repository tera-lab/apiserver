class LfgController < Sinatra::Base
  get '/party_match_info' do
    headers 'Access-Control-Allow-Origin' => '*'
    json(settings.cache.get('party_match_info') || {
      lfgList: [],
      updated_at: nil
    })
  end

  post '/party_match_info' do
    validates do
      required(:playerId).filled(:int?, gt?: 0)
      required(:lfgList).each do
        schema do
          required(:isRaid).filled(:int?)
          required(:playerCount).filled(:int?)
          required(:message).filled(:str?)
          required(:leader).filled(:str?)
        end
      end
    end

    data = {
      lfgList: params[:lfgList],
      updated_at: Time.now
    }
    settings.cache.set('party_match_info', data)
    
    json ({
      success: 'updated'
    })
  end

  post '/party_match_link' do  
    validates do
      configure do
        def self.messages
          super.merge(
            en: {errors: {
              check_spam_user: 'he is spam user',
              check_spam_message: 'message contains spam word'
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

        validate(check_spam_user: :name) do |name|
          name.normalize != 'あるていしあ' &&
          name.normalize !~ /^知.+ちゃん$/
        end

        validate(check_spam_message: :message) do |_|
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

    json ({
      success: 'updated'
    })
  end
end