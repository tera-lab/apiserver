class String
  require 'nkf'

  def normalize
    NKF.nkf('-w --hiragana', self.downcase)
  end
end