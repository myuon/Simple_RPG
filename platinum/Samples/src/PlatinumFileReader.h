// ppj file import sample.
#ifndef __CLASS_PLATINUM_PROJECT_FILE_READER_H__
#define __CLASS_PLATINUM_PROJECT_FILE_READER_H__

#include <windows.h>
#include <string>
#include <vector>

namespace platinum {

struct Chunk
{
	DWORD dwID;
	DWORD dwSize;
};

struct UMFHeader
{
	DWORD dwMapWidth;
	DWORD dwMapHeight;
	DWORD dwChipWIdth;
	DWORD dwChipHeight;
	BYTE byLayerCount;
	BYTE byBitCount;
	BYTE byRelativePath;
	BYTE reserved;
};

struct FileVersion
{
	BYTE byMajor;	// �����_�ȏ�
	BYTE byMinor;	// �����_�ȉ�
	BYTE byRelease;	// �����_���ʈȉ�
	char cAlpha;	// �C�ӕ���(1����)
};

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
	void* pData;	// �f�[�^
};

struct Layer
{
	typedef std::vector<WORD> WordArray;
	std::string	strName;
	std::string	strImage;
	BOOL		bVisible;
	WordArray	arrData;
};
typedef std::vector<Layer*> LayerArray;
typedef LayerArray::iterator LayerArrayItor;

class PlatinumFileReader
{
	UMFHeader		_header;
	std::string		_strComment;
	LayerArray		_layers;
	Colorkey		_colorkey;
	InvisiblePatrs	_inv;
//	GridColor		_grid;
//	EditorEnv		_env;
//	FileVersion		_version;
//	WORD			_wZoomRatio;
//	std::vector<BYTE>	_hidden;
public:
	~PlatinumFileReader();
	
	BOOL Open(const char* szFilePath);
	void Close();
	bool IsOpen() { return !_layers.empty(); }

	DWORD GetMapWidth() const 		{ return _header.dwMapWidth; }
	DWORD GetMapHeight() const		{ return _header.dwMapHeight; }
	DWORD GetChipWidth() const 		{ return _header.dwChipWIdth; }
	DWORD GetChipHeight() const 	{ return _header.dwChipHeight; }
	BYTE GetBitCount() const 		{ return _header.byBitCount; }
	BYTE GetLayerCount() const 		{ return _header.byLayerCount; }
	bool IsRelativePath() const 	{ return _header.byRelativePath == 1 ? true : false; }

	bool UseColorkey() const 		{ return _colorkey.byUse == 1 ? true : false; }
	DWORD GetColorkey() const 		{ return _colorkey.dwColor; }

	bool UseInvisibleNumber() const { return _inv.byUse == 1 ? true : false; }
	WORD GetInvisibleNumber() const { return _inv.wInvisible; }

	WORD* GetLayerAddr(BYTE byLayer) const				{ return &_layers[byLayer]->arrData[0]; }
	const char* GetLayerName(BYTE byLayer) const		{ return _layers[byLayer]->strName.c_str(); }
	const char* GetLayerImagePath(BYTE byLayer) const	{ return _layers[byLayer]->strImage.c_str(); }

	const char* GetComment() const { return _strComment.c_str(); }

	int GetValue(BYTE byLayerIndex, DWORD dwX, DWORD dwY) const
	{
		int nIndex = -1;

		// �͈̓`�F�b�N
		if (byLayerIndex >= GetLayerCount() ||
			dwX >= GetMapWidth() ||
			dwY >= GetMapHeight())
			return nIndex;

		if (GetBitCount() == 8) {
			// 8bit layer
			BYTE* pLayer = (BYTE*)GetLayerAddr(byLayerIndex);
			nIndex = *(pLayer + dwY * GetMapWidth() + dwX);
		} else {
			// 16bit layer	
			WORD* pLayer = (WORD*)GetLayerAddr(byLayerIndex);
			nIndex = *(pLayer + dwY * GetMapWidth() + dwX);
		}

		return nIndex;
	}
	
	void SetValue(BYTE byLayerIndex, DWORD dwX, DWORD dwY, int nValue)
	{
		// �͈̓`�F�b�N
		if (byLayerIndex >= GetLayerCount() ||
			dwX >= GetMapWidth() ||
			dwY >= GetMapHeight())
			return;

		if (GetBitCount() == 8)
		{
			// 8bit layer
			BYTE* pLayer = (BYTE*)GetLayerAddr(byLayerIndex);
			*(pLayer + dwY * GetMapWidth() + dwX) = (BYTE)nValue;
		}
		else
		{
			// 16bit layer	
			WORD* pLayer = (WORD*)GetLayerAddr(byLayerIndex);
			*(pLayer + dwY * GetMapWidth() + dwX) = (WORD)nValue;
		}
	}
private:
	DWORD FindChunk(HANDLE hFile, int nFindFrom, const char* szChunkID);
	void SkipNullByte(HANDLE hFile, const Chunk& ck);
	bool ReadString(HANDLE hFile, const Chunk& ck, std::string& str);
};

} // namespace platinum
#endif // __CLASS_PLATINUM_PROJECT_FILE_H__

































