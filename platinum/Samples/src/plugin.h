
// Platinum Plug-In(ppi) definition file

#include <windows.h>
#pragma once

// Plugin����
#define PPITYPE_IMPORT			0x01	// �v���O�C����Import�֐����T�|�[�g���܂�
#define PPITYPE_EXPORT			0x02	// �v���O�C����Export�֐����T�|�[�g���܂�
#define PPITYPE_FILEFORMAT		0x04	// �v���O�C���̓t�@�C���t�H�[�}�b�g�Ƃ��ċ@�\���܂�
#define PPITYPE_HASCONFIG		0x08	// �R���t�B�O��ʂ�����
//#define PPITYPE_COMMAND		0x10	

// �v���O���X�R�[���o�b�N���Ԃ��߂�l
#define PPICALLBACK_ABORT		0	// ���[�U�����~��I�������i���₩�ɏ����𒆒f���ĉ������j
#define PPICALLBACK_OK			1	// OK.�i�����𑱍s���ĉ������j

// �Ăяo�����֕ԋp����߂�l
#define PPIRET_OK				0	// ����I��
#define PPIRET_UNSUPPORTED		1	// ���̃t�@�C���̓T�|�[�g���Ă��܂���
#define PPIRET_NOTIMPLEMENTED	2	// �������̊֐��ł�
#define PPIRET_INVALIDPARAMS	3	// �������s���ł�
#define PPIRET_INVALIDFILE		4	// �t�@�C�����j�����Ă��܂�
#define PPIRET_FILEERR			5	// �t�@�C���G���[���������܂���
#define PPIRET_OUTOFMEMORY		6	// ���������s�����Ă��܂�
#define PPIRET_ABORT			7	// �R�[���o�b�N�֐�����PPICALLBACK_ABORT���󂯎�����̂ŏ����𒆎~���܂���
#define PPIRET_INTERNALERR		8	// �����G���[���������܂���

/*
#define PPIEVENT_LOAD				0	// �v���O�C�����ǂݍ��܂ꂽ
#define PPIEVENT_MAP_OPEN			1	
#define PPIEVENT_MAP_CLOSE			2
#define PPIEVENT_SEL_CHANGED		3	// �I����Ԃ��ύX���ꂽ
#define PPIEVENT_DATA_MODIFY		4	// �}�b�v�f�[�^���ύX���ꂽ
#define PPIEVENT_CURSOR_MOVE		5
#define PPIEVENT_CHIP_CHANGED		6
#define PPIEVENT_LAYER_CHANGED		7	// ���C���[�̑I�����ύX���ꂽ
#define PPIEVENT_LAYER_VISIBLE		8	// ���C���[�̉���Ԃ��ύX���ꂽ
#define PPIEVENT_LAYER_MOVED		9	// ���C���[�̏��Ԃ��ύX���ꂽ
#define PPIEVENT_LAYER_NEW			10	// �V�������C���[���쐬���ꂽ
#define PPIEVENT_LAYER_DELETE		11	// ���C���[���폜���ꂽ
#define PPIEVENT_LAYER_CHANGE_PARTS	12	// ���C���[�̃p�[�c�Z�b�g���ύX���ꂽ
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

// LPARAM : �I��͈͂̏����擾
#define WM_PPI_GET_SELECT_AREA_INFO	(WM_PPI_FIRST + 100)
#define Platinum_GetSelectArea(hWnd, pSelectAreaInfo) \
	(UINT)SendMessage((hWnd), WM_PPI_GET_SELECT_AREA_INFO, 0, (LPARAM)(SelectAreaInfo*)pSelectAreaInfo)

// LPARAM : �I��͈͂̏���ݒ�
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

// �v���O���X�o�[���������邽�߂̃R�[���o�b�N�֐�
// nNow		���݂̏����P��
// nMax		�����P�ʂ̍ő�l
// lpszMsg	�������e��ʒm���邽�߂̃��b�Z�[�W�i���b�Z�[�W�������ꍇ��NULL��n���܂��j
typedef BYTE (__stdcall* PPI_PROGRESS_CALLBACK)(int nNow, int nMax, LPCTSTR lpszMsg);

#pragma pack(push, 1)
struct PlatinumPluginInfo
{
	char szPluginName[128];		// �v���O�C���̖��O
	char szFileFilter[128];		// �T�|�[�g����t�@�C���̃t�B���^������
	DWORD dwFlags;				// �t���O(PPITYPE_IMPORT and(or) PPITYPE_EXPORT or PPITYPE_FILEFORMAT)
};

// Platinum���Ǘ�����f�[�^�\��
// Export���ɂ͂��̃f�[�^�\����C�ӂ̌`�ŏo�͂��ĉ�����
// Import���ɂ͕K�v�ɉ����ă������[�����蓖�ăf�[�^��ǂݍ���ŉ�����
struct PlatinumData
{
	// �K�{�f�[�^
	struct Important
	{
		struct Header
		{
			DWORD dwMapWidth;		// �}�b�v�̉���
			DWORD dwMapHeight;		// �}�b�v�̍���
			DWORD dwChipWidth;		// �`�b�v(�p�[�c)�̉���
			DWORD dwChipHeight;		// �`�b�v(�p�[�c)�̍���
			BYTE byLayerCount;		// ���C����(1�ȏ�)
			BYTE byBitCount;		// 1�`�b�v�̃f�[�^��(8 or 16)
			BYTE byRelativePath;	// 0 = �p�X���t�@�C�����݂̂Ŋi�[, 1 = �p�X�𑊑΃p�X�Ŋi�[
			BYTE byOption;			// 0 = �I�v�V�����Ȃ�, 1 = �`�b�v�̃A���C�����g���Œ�(ver1.68)
		};
		struct Layer
		{
			LPTSTR lpszLayerName;		// ���C�����B�C�ӂ̖��O�ɂ���ꍇ��NULL���w��\(��1���Q�Ɓj
			LPTSTR lpszLayerChipName;	// �摜�̃p�X�B���蓖�ĂȂ��ꍇ��NULL���w��\(��1���Q�Ɓj
			BYTE	byVisible;			// �����
			WORD*	pData;				// �}�b�v�z��(��1���Q�Ɓj
		};
		Header	header;
		Layer*	pLayers;	// ���C���z��(��1���Q�Ɓj
	} important;

	// �I�v�V�����f�[�^
	struct Optional
	{
		struct Colorkey
		{
			BYTE byUse;		// ���ߏ���(0 = ���� / 1 = �L��)
			DWORD dwColor;	// ���ߐF
			BYTE reserved;	// �\��
		};
		struct InvisiblePatrs
		{
			BYTE byUse;			// �����p�[�c(0 = ���� / 1 = �L��)
			WORD wInvisible;	// �����p�[�c�ԍ�
			BYTE reserved;		// �\��
		};
		struct EditorEnv
		{
			BYTE byShowGrid;		// �O���b�h(0 = ��\�� / 1 = �\��)
			BYTE byShowData;		// �p�[�c�ԍ�(0 = ��\�� / 1 = �\��)
			BYTE byShowIndex;		// �g�p���܂���
			BYTE byShowCursorGrid;	// �J�[�\���O���b�h(0 = ��\�� / 1 = �\��)
			BYTE byShowMarker;		// �}�[�J�[(0 = ��\�� / 1 = �\��)
			BYTE byShowFog;			// �t�H�O���[�h(0 = ���� / 1 = �L��)
		};
		struct GridColor
		{
			DWORD dwGridColor;	// �O���b�h�̐F
			DWORD dwCGridColor;	// �J�[�\���O���b�h�̐F
		};
		struct HiddenData
		{
			DWORD dwSize;	// �f�[�^�̃T�C�Y(dwSize == 0 �̏ꍇ pData == NULL �ł�)
			void* pData;	// �f�[�^(��1���Q��)
		};

		EditorEnv		env;
		Colorkey		colorkey;
		InvisiblePatrs	invisible;
		GridColor		gridColor;
		WORD			wZoomRatio;
		LPTSTR			lpszComment;	// �}�b�v�R�����g(��1���Q��)
		HiddenData		hidden;			// ���[�U�f�[�^(��2���Q��)
	} optional;
};
#pragma pack(pop)

	// ��1
	// Import���ɂ�GlobalAlloc(GPTR, size)�ɂă������[���蓖�Ă��s���Ă��������B
	// �������[�̊J���͌Ăяo�����ōs���Ă���̂Ŋ֐����甲����O�ɊJ�����Ȃ��ł��������B
	// �G���[�����������ꍇ�̓v���O�C�����œK�؂Ƀ������[���J�����Ă��������B

	// ��2
	// �t�@�C�������R�Ƀf�[�^���i�[���鎖���o����̈�ł��B
	// Import���ɂ��̗̈�ɃT�C�Y�ƃf�[�^��ݒ肷�鎖�ɂ��Platinum���ɕێ�����A
	// Export���ɍēx���̃f�[�^���v���O�C���Ɉ����n����̂Ńt�@�C���ɋL�^����Ȃǂ��ĉ������B
	// ����͎�Ƀv���O�C�����ŕ\�������_�C�A���O�Ȃǂ�����͂��ꂽ�f�[�^��ۑ�����ꍇ�Ɏg�p����܂��B

