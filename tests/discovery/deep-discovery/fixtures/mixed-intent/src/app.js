const referral = { id: "R-17", score: 92 };

function review(item) {
  return {
    ...item,
    status: "pending-manual-review",
    destination: "local-json-file",
  };
}

console.log(JSON.stringify(review(referral)));
