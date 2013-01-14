
// Platinum Plug-In(ppi) definition file

#include <windows.h>
#pragma once

// Plugin特性
#define PPITYPE_IMPORT			0x01	// プラグインはImport関数をサポートします
#define PPITYPE_EXPORT			0x02	// プラグインはExport関数をサポートします
#define PPITYPE_FILEFORMAT		0x04	// プラグインはファイルフォーマットとして機能します
#define PPITYPE_HASCONFIG		0x08	// コンフィグ画面を持つ
//#define PPITYPE_COMMAND		0x10	

// プログレスコールバックが返す戻り値
#define PPICALLBACK_ABORT		0	// ユーザが中止を選択した（速やかに処理を中断して下さい）
#define PPICALLBACK_OK			1	// OK.（処理を続行して下さい）

// 呼び出し元へ返却する戻り値
#define PPIRET_OK				0	// 正常終了
#define PPIRET_UNSUPPORTED		1	// このファイルはサポートしていません
#define PPIRET_NOTIMPLEMENTED	2	// 未実装の関数です
#define PPIRET_INVALIDPARAMS	3	// 引数が不正です
#define PPIRET_INVALIDFILE		4	// ファイルが破損しています
#define PPIRET_FILEERR			5	// ファイルエラーが発生しました
#define PPIRET_OUTOFMEMORY		6	// メモリが不足しています
#define PPIRET_ABORT			7	// コールバック関数からPPICALLBACK_ABORTを受け取ったので処理を中止しました
#define PPIRET_INTERNALERR		8	// 内部エラーが発生しました

/*
#define PPIEVENT_LOAD				0	// プラグインが読み込まれた
#define PPIEVENT_MAP_OPEN			1	
#define PPIEVENT_MAP_CLOSE			2
#define PPIEVENT_SEL_CHANGED		3	// 選択状態が変更された
#define PPIEVENT_DATA_MODIFY		4	// マップデータが変更された
#define PPIEVENT_CURSOR_MOVE		5
#define PPIEVENT_CHIP_CHANGED		6
#define PPIEVENT_LAYER_CHANGED		7	// レイヤーの選択が変更された
#define PPIEVENT_LAYER_VISIBLE		8	// レイヤーの可視状態が変更された
#define PPIEVENT_LAYER_MOVED		9	// レイヤーの順番が変更された
#define PPIEVENT_LAYER_NEW			10	// 新しいレイヤーが作成された
#define PPIEVENT_LAYER_DELETE		11	// レイヤーが削除された
#define PPIEVENT_LAYER_CHANGE_PARTS	12	// レイヤーのパーツセットが変更された
*/
/*
struct SelectAreaInfo
{
	BOOL bSelected;
	POINT pos;
	SIZE size;
	int nStartIndex;
};

#define WM_PPI_FIRST           (WM_APP + 0)

// return : (UINT)map_width
#define WM_PPI_GETMAPWIDTH     (WM_PPI_FIRST)
#define Platinum_GetMapWidth(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GETMAPWIDTH, 0, 0)

// return : (UINT)map_height
#define WM_PPI_GETMAPHEIGHT    (WM_PPI_FIRST + 1)
#define Platinum_GetMapHeight(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GETMAPHEIGHT, 0, 0)

// return : (UINT)chip_width
#define WM_PPI_GETCHIPWIDTH    (WM_PPI_FIRST + 2)
#define Platinum_GetChipWidth(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GETCHIPWIDTH, 0, 0)

// return : (UINT)chip_height
#define WM_PPI_GETCHIPHEIGHT   (WM_PPI_FIRST + 3)
#define Platinum_GetChipHeight(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GETCHIPHEIGHT, 0, 0)

// return : (UINT)bitcount
#define WM_PPI_GET_BITCOUNT   (WM_PPI_FIRST + 4)
#define Platinum_GetBitCount(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_BITCOUNT, 0, 0)

// return : (UINT)layer_count
#define WM_PPI_GET_LAYER_COUNT   (WM_PPI_FIRST + 5)
#define Platinum_GetLayerCount(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_LAYER_COUNT, 0, 0)

// return : (UINT)chip_path_type
#define WM_PPI_GET_PATH_TYPE   (WM_PPI_FIRST + 6)
#define Platinum_GetPathType(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_PATH_TYPE, 0, 0)

// return : (UINT)chip_align_type
#define WM_PPI_GET_CHIP_ALIGN_TYPE   (WM_PPI_FIRST + 7)
#define Platinum_GetChipAlignType(hWnd) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_CHIP_ALIGN_TYPE, 0, 0)

// (GET_LAYER_STRING_INFO)wParam = pLayerStringInfo;
// return : (UINT)pLayerStringInfo->nBufferSize;
struct GET_LAYER_STRING_INFO
{
	int nLayer;
	int nBufferSize;
};
#define WM_PPI_GET_LAYER_NAME   (WM_PPI_FIRST + 8)
#define Platinum_GetLayerName(hWnd, pLayerStringInfo, lpszBuffer) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_LAYER_NAME, (WPARAM)pLayerStringInfo, (LPARAM)lpszBuffer)

// (GET_LAYER_STRING_INFO)wParam = pLayerStringInfo;
// return : (UINT)pLayerStringInfo->nBufferSize;
#define WM_PPI_GET_LAYER_CHIP_PATH   (WM_PPI_FIRST + 9)
#define Platinum_GetLayerChipPath(hWnd, pLayerStringInfo, lpszBuffer) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_LAYER_CHIP_PATH, (WPARAM)pLayerStringInfo, (LPARAM)lpszBuffer)

// (UINT)wParam = nLayer;
// return : (BOOL)bLayerVisibled;
#define WM_PPI_GET_LAYER_VISIBLE_STATE   (WM_PPI_FIRST + 10)
#define Platinum_GetLayerVisibleState(hWnd, nLayer) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_LAYER_VISIBLE_STATE, (WPARAM)nLayer, (LPARAM)0)

// LPARAM : 選択範囲の情報を取得
#define WM_PPI_GET_SELECT_AREA_INFO	(WM_PPI_FIRST + 100)
#define Platinum_GetSelectArea(hWnd, pSelectAreaInfo) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_SELECT_AREA_INFO, 0, (LPARAM)(SelectAreaInfo*)pSelectAreaInfo)

// LPARAM : 選択範囲の情報を設定
#define WM_PPI_SET_SELECT_AREA_INFO	(WM_PPI_FIRST + 101)
#define Platinum_SetSelectArea(hWnd, pSelectAreaInfo) \
	(UINT)SendMessage((hWnd), WM_PPI_SET_SELECT_AREA_INFO, 0, (LPARAM)(SelectAreaInfo*)pSelectAreaInfo)

// Platinum_GetLayerData(HWND hWnd, PPI_GETDATA_STRUCT* pStruct);
#define WM_PPI_GET_LAYER_DATA	(WM_PPI_FIRST + 102)
struct PPI_GET_LAYER_DATA_INFO
{
	int nSize;		// in: sizeof(PPI_GETDATA_STRUCT)
	int nLayer;		// in: 
	int nDataSize;	// in: size of pData
	void* pData;	// out:
};
#define Platinum_GetLayerData(hWnd, pGetLayerDataInfo, pBuffer) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_LAYER_DATA, (WPARAM)pGetLayerDataInfo, (LPARAM)pBuffer)

#define WM_PPI_SET_LAYER_DATA	(WM_PPI_FIRST + 103)
#define Platinum_SetLayerData(hWnd, pData, nLength) \
	(UINT)SendMessage((hWnd), WM_PPI_SET_LAYER_DATA, (WPARAM)nLength, (LPARAM)pData)

#define WM_PPI_GET_CHIPHANDLE (WM_PPI_FIRST + 200)
#pragma pack(push, 1)
struct GET_CHIPHANDLE_STRUCT
{
	int nSize;
	int nLayer;
	int nImageWidth;
	int nImageHeight;
	HBITMAP hBitmap;
	char strImagePath[512];
};
#pragma pack(pop)
#define Platinum_GetChipHandle(hWnd, pStruct) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_CHIPHANDLE, 0, (LPARAM)(pStruct))
*/


#define SAFE_GLOBAL_FREE(p) if (p != NULL) { ::GlobalFree(p); p = NULL; }

// プログレスバーを処理するためのコールバック関数
// nNow		現在の処理単位
// nMax		処理単位の最大値
// lpszMsg	処理内容を通知するためのメッセージ（メッセージが無い場合はNULLを渡せます）
typedef BYTE (__stdcall* PPI_PROGRESS_CALLBACK)(int nNow, int nMax, LPCTSTR lpszMsg);

#pragma pack(push, 1)
struct PlatinumPluginInfo
{
	char szPluginName[128];		// プラグインの名前
	char szFileFilter[128];		// サポートするファイルのフィルタ文字列
	DWORD dwFlags;				// フラグ(PPITYPE_IMPORT and(or) PPITYPE_EXPORT or PPITYPE_FILEFORMAT)
};

// Platinumが管理するデータ構造
// Export時にはこのデータ構造を任意の形で出力して下さい
// Import時には必要に応じてメモリーを割り当てデータを読み込んで下さい
struct PlatinumData
{
	// 必須データ
	struct Important
	{
		struct Header
		{
			DWORD dwMapWidth;		// マップの横幅
			DWORD dwMapHeight;		// マップの高さ
			DWORD dwChipWidth;		// チップ(パーツ)の横幅
			DWORD dwChipHeight;		// チップ(パーツ)の高さ
			BYTE byLayerCount;		// レイヤ数(1以上)
			BYTE byBitCount;		// 1チップのデータ量(8 or 16)
			BYTE byRelativePath;	// 0 = パスをファイル名のみで格納, 1 = パスを相対パスで格納
			BYTE byOption;			// 0 = オプションなし, 1 = チップのアライメントを非固定(ver1.68)
		};
		struct Layer
		{
			LPTSTR lpszLayerName;		// レイヤ名。任意の名前にする場合はNULLを指定可能(※1を参照）
			LPTSTR lpszLayerChipName;	// 画像のパス。割り当てない場合はNULLを指定可能(※1を参照）
			BYTE	byVisible;			// 可視状態
			WORD*	pData;				// マップ配列(※1を参照）
		};
		Header	header;
		Layer*	pLayers;	// レイヤ配列(※1を参照）
	} important;

	// オプションデータ
	struct Optional
	{
		struct Colorkey
		{
			BYTE byUse;		// 透過処理(0 = 無効 / 1 = 有効)
			DWORD dwColor;	// 透過色
			BYTE reserved;	// 予約
		};
		struct InvisiblePatrs
		{
			BYTE byUse;			// 透明パーツ(0 = 無効 / 1 = 有効)
			WORD wInvisible;	// 透明パーツ番号
			BYTE reserved;		// 予約
		};
		struct EditorEnv
		{
			BYTE byShowGrid;		// グリッド(0 = 非表示 / 1 = 表示)
			BYTE byShowData;		// パーツ番号(0 = 非表示 / 1 = 表示)
			BYTE byShowIndex;		// 使用しません
			BYTE byShowCursorGrid;	// カーソルグリッド(0 = 非表示 / 1 = 表示)
			BYTE byShowMarker;		// マーカー(0 = 非表示 / 1 = 表示)
			BYTE byShowFog;			// フォグモード(0 = 無効 / 1 = 有効)
		};
		struct GridColor
		{
			DWORD dwGridColor;	// グリッドの色
			DWORD dwCGridColor;	// カーソルグリッドの色
		};
		struct HiddenData
		{
			DWORD dwSize;	// データのサイズ(dwSize == 0 の場合 pData == NULL です)
			void* pData;	// データ(※1を参照)
		};

		EditorEnv		env;
		Colorkey		colorkey;
		InvisiblePatrs	invisible;
		GridColor		gridColor;
		WORD			wZoomRatio;
		LPTSTR			lpszComment;	// マップコメント(※1を参照)
		HiddenData		hidden;			// ユーザデータ(※2を参照)
	} optional;
};
#pragma pack(pop)

	// ※1
	// Import時にはGlobalAlloc(GPTR, size)にてメモリー割り当てを行ってください。
	// メモリーの開放は呼び出し側で行っているので関数から抜ける前に開放しないでください。
	// エラーが発生した場合はプラグイン側で適切にメモリーを開放してください。

	// ※2
	// ファイルが自由にデータを格納する事が出来る領域です。
	// Import時にこの領域にサイズとデータを設定する事によりPlatinum内に保持され、
	// Export時に再度このデータがプラグインに引き渡さるのでファイルに記録するなどして下さい。
	// これは主にプラグイン側で表示したダイアログなどから入力されたデータを保存する場合に使用されます。

