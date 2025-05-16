<body onkeydown="checkKey(event)">
<script>
let keys = [];
const code = "38384040373937396665"; // Up Up Down Down Left Right Left Right B A
function checkKey(e) {
  keys.push(e.keyCode);
  if (keys.join('').includes(code)) {
    alert("🎉 You unlocked a secret!");
    keys = [];
  }
}
</script>
</body>
