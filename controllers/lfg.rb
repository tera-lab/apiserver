class LfgController < Sinatra::Base  
  get '/party_match_info' do
    headers 'Access-Control-Allow-Origin' => '*'
    json({
      lfgList: settings.cache.get('party_match_info.lfgList') || [],
      updated_at: settings.cache.get('party_match_info.updated_at')
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

    settings.cache.set('party_match_info.lfgList', params[:lfgList], 180)
    settings.cache.set('party_match_info.updated_at', Time.now)
    
    json ({
      success: 'updated'
    })
  end

  post '/party_match_link' do
    halt 410
  end
end