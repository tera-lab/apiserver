class GuildBamController < Sinatra::Base
  def monster_name
    hour = Time.now.hour
    raise if hour > 22
    case Date.today.wday
    when 1, 4
      raise if hour < 12
      "虐殺のサブラニア"
    when 2, 5
      raise if hour < 18
      "貪欲のアナンシャ(vP)"
    when 0, 3
      raise if hour < 18
      "激昂のカラゴス"
    when 6
      raise
    end
  rescue
    nil
  end

  post '/gquest_urgent_notify' do
    validates do
      required(:content).filled(:str?, format?: /^.+(?<!\(Test message\))$/i)
    end

    settings.mutex.synchronize do
      halt 429 if settings.cache.get('gquest_urgent_notify')
    end
    settings.cache.set('gquest_urgent_notify', true, 180)

    bam = monster_name()
    halt if bam.nil?

    settings.gb_webhooks.each do |hook|
      HTTP.post(hook, json:{
        content: "@here まもなく#{bam}が出現します"
      })
    end
  end
end