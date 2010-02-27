window.addEvent('domready', function(){
  updateShortcutTitles();
  $('lexer').addEvent('change', rebuildLexerIntoText);
});
