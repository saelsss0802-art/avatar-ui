/**
 * Grok API プロキシ - Cloudflare Workers
 * Robloxからのリクエストを受け取り、Grok APIに転送する
 */

export default {
  async fetch(request, env) {
    // CORSヘッダー（Robloxからのアクセスを許可）
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    // OPTIONSリクエスト（プリフライト）への対応
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // POSTリクエストのみ許可
    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405, headers: corsHeaders });
    }

    try {
      // Robloxからのリクエストボディを取得
      const body = await request.json();

      // システムプロンプト（SPECTRAの人格）- wrangler.tomlで設定
      const systemPrompt = env.SYSTEM_PROMPT;
      
      // APIリクエストボディを構築
      const apiBody = {
        model: env.GROK_MODEL || "grok-4-1-fast-non-reasoning",
        input: [
          { role: "user", content: body.prompt || "Hello" },
        ],
      };

      // 会話継続の場合: previous_response_idを追加
      if (body.previous_response_id) {
        apiBody.previous_response_id = body.previous_response_id;
      } else {
        // 新規会話: システムプロンプトを先頭に追加
        apiBody.input.unshift({ role: "system", content: systemPrompt });
      }

      // Grok APIに転送
      const grokResponse = await fetch("https://api.x.ai/v1/responses", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${env.XAI_API_KEY}`,
        },
        body: JSON.stringify(apiBody),
      });

      // Grok APIのレスポンスを取得
      const grokData = await grokResponse.json();

      // デバッグ用：APIエラーチェック
      if (grokData.error) {
        return new Response(JSON.stringify({
          success: false,
          error: grokData.error,
        }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      // テキスト部分を抽出して返す
      let text = "";
      if (grokData.output && grokData.output[0] && grokData.output[0].content) {
        const textContent = grokData.output[0].content.find(c => c.type === "output_text");
        if (textContent) {
          text = textContent.text;
        }
      }

      // Robloxに返す
      return new Response(JSON.stringify({
        success: true,
        text: text,
        response_id: grokData.id,
      }), {
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      });

    } catch (error) {
      // エラー時
      return new Response(JSON.stringify({
        success: false,
        error: error.message,
      }), {
        status: 500,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      });
    }
  },
};
