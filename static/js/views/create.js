window.addEvent('domready', function(){
  updateShortcutTitles();
  $('code').focus();
  $('lexer').addEvent('change', rebuildLexerIntoText);
});
