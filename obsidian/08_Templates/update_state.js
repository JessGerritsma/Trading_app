module.exports = async (tp) => {
  const { exec } = require('child_process');
  exec('python3 auto_update_state.py', (error, stdout, stderr) => {
    if (error) {
      new Notice(`Error: ${error.message}`);
      return;
    }
    if (stderr) {
      new Notice(`Warning: ${stderr}`);
      return;
    }
    new Notice('✅ _current_state.md updated!');
    console.log(stdout);
  });
};
